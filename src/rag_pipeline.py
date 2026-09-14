from pathlib import Path

from config.settings import settings
from src.embeddings import EmbeddingEngine
from src.llm import LLMClient
from src.vector_store import VectorStore
from utils.file_utils import load_all_documents, split_into_paragraphs
from utils.logger import get_logger


logger = get_logger(__name__)

INDEX_DIR = Path("index")


class RAGPipeline:
    """
    Retrieval-Augmented Generation pipeline.

    Combines semantic search (FAISS) with LLM-based answer generation to
    produce accurate, source-aware answers to user questions.

    Workflow:
    1. build()  — loads documents, generates embeddings, builds FAISS index.
    2. query()  — embeds the question, retrieves top-K paragraphs from FAISS,
                  passes them to the LLM to generate a final answer.

    Semantic search works without an API key.
    Answer generation requires GEMINI_API_KEY to be set in the .env file.
    """

    def __init__(self, data_dir: Path = settings.data_path) -> None:
        """
        Args:
            data_dir: Path to the directory containing .txt document files.
        """
        self._data_dir = data_dir
        self._embedding_engine = EmbeddingEngine()
        self._vector_store = VectorStore()
        self._llm: LLMClient | None = None
        self._is_built = False

    def build(self, force_rebuild: bool = False) -> None:
        """
        Loads documents, generates embeddings, and builds the FAISS index.

        If a saved index already exists in the index/ directory and
        force_rebuild is False, the saved index is loaded instead of rebuilding.
        This avoids regenerating embeddings on every startup.

        Args:
            force_rebuild: If True, always rebuilds the index even if a saved
                          version exists. Defaults to False.
        """
        if not force_rebuild and INDEX_DIR.exists():
            try:
                self._vector_store.load(INDEX_DIR)
                self._is_built = True
                logger.info("Loaded existing FAISS index from disk.")
                return
            except FileNotFoundError:
                logger.info("No saved index found. Building from scratch.")

        logger.info("Building RAG pipeline index from documents in: %s", self._data_dir)

        documents = load_all_documents(self._data_dir)
        if not documents:
            logger.warning("No documents found. RAG pipeline index is empty.")
            self._is_built = True
            return

        all_paragraphs: list[str] = []
        all_sources: list[str] = []

        for filename, content in documents.items():
            paragraphs = split_into_paragraphs(content)
            all_paragraphs.extend(paragraphs)
            all_sources.extend([filename] * len(paragraphs))

        logger.info(
            "Generating embeddings for %d paragraph(s) across %d document(s).",
            len(all_paragraphs),
            len(documents),
        )

        embeddings = self._embedding_engine.embed_texts(all_paragraphs)
        self._vector_store.build(embeddings, all_paragraphs, all_sources)
        self._vector_store.save(INDEX_DIR)

        self._is_built = True
        logger.info("RAG pipeline index built and saved.")

    def semantic_search(self, question: str, top_k: int = settings.TOP_K) -> list[dict]:
        """
        Searches for paragraphs semantically similar to the question.

        This method works without an LLM API key.

        Args:
            question: Raw question or query string.
            top_k:    Number of top results to return.

        Returns:
            List of result dicts with "paragraph", "source", and "score" keys.
            Results are ordered by similarity score (highest first).
        """
        if not self._is_built:
            logger.error("RAG pipeline is not built. Call build() first.")
            return []

        query_embedding = self._embedding_engine.embed_query(question)
        results = self._vector_store.search(query_embedding, top_k=top_k)
        logger.info("Semantic search returned %d result(s) for: %r", len(results), question)
        return results

    def query(self, question: str, top_k: int = settings.TOP_K) -> dict:
        """
        Answers a question using retrieval-augmented generation.

        Retrieves the top_k most relevant paragraphs using semantic search,
        then passes them as context to the Gemini LLM to generate an answer.

        Requires GEMINI_API_KEY to be set in the .env file.

        Args:
            question: The user's question.
            top_k:    Number of context paragraphs to retrieve.

        Returns:
            Dict containing:
            - "answer":  Generated answer string from the LLM.
            - "sources": List of result dicts used as context.

        Raises:
            ValueError: If GEMINI_API_KEY is not configured.
            RuntimeError: If the LLM call fails.
        """
        if not settings.llm_available:
            raise ValueError(
                "LLM features are not available. "
                "Set GEMINI_API_KEY in your .env file to enable answer generation."
            )

        if self._llm is None:
            self._llm = LLMClient(api_key=settings.GEMINI_API_KEY)

        context = self.semantic_search(question, top_k=top_k)
        answer = self._llm.generate_answer(question, context)

        return {
            "answer": answer,
            "sources": context,
        }

    @property
    def is_built(self) -> bool:
        """Returns True if the pipeline index has been built."""
        return self._is_built

    @property
    def vector_store_size(self) -> int:
        """Returns the number of indexed paragraphs."""
        return self._vector_store.size
