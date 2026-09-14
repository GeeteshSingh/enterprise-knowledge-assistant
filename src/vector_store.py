import pickle
from pathlib import Path

import numpy as np

from utils.logger import get_logger


logger = get_logger(__name__)


class VectorStore:
    """
    FAISS-based vector store for storing and searching paragraph embeddings.

    Stores embeddings alongside their corresponding paragraph texts and source
    filenames so that search results are self-contained.

    The index uses inner product similarity. Since embeddings are L2-normalized
    by the EmbeddingEngine, inner product is equivalent to cosine similarity.
    """

    def __init__(self) -> None:
        self._index = None
        self._paragraphs: list[str] = []
        self._sources: list[str] = []
        self._is_built = False

    def build(
        self,
        embeddings: np.ndarray,
        paragraphs: list[str],
        sources: list[str],
    ) -> None:
        """
        Builds the FAISS index from paragraph embeddings.

        Args:
            embeddings: Float32 array of shape (n_paragraphs, embedding_dim).
            paragraphs: List of paragraph strings corresponding to each embedding.
            sources:    List of source filenames corresponding to each paragraph.

        Raises:
            ValueError: If embeddings, paragraphs, and sources have different lengths.
        """
        import faiss

        if not (len(embeddings) == len(paragraphs) == len(sources)):
            raise ValueError(
                "embeddings, paragraphs, and sources must have the same length."
            )

        embedding_dim = embeddings.shape[1]
        self._index = faiss.IndexFlatIP(embedding_dim)
        self._index.add(embeddings)
        self._paragraphs = list(paragraphs)
        self._sources = list(sources)
        self._is_built = True

        logger.info(
            "FAISS index built: %d vectors, %d dimensions.",
            len(paragraphs),
            embedding_dim,
        )

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Searches the index for the top_k most similar paragraphs.

        Args:
            query_embedding: Float32 array of shape (1, embedding_dim).
            top_k:           Number of top results to return.

        Returns:
            List of result dicts, each containing:
            - "paragraph": The matching paragraph text.
            - "source":    The source filename.
            - "score":     Cosine similarity score (float between 0 and 1).

        Returns an empty list if the index has not been built.
        """
        if not self._is_built:
            logger.error("VectorStore has not been built. Call build() first.")
            return []

        k = min(top_k, len(self._paragraphs))
        scores, indices = self._index.search(query_embedding, k)

        results = []
        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue
            results.append(
                {
                    "paragraph": self._paragraphs[index],
                    "source": self._sources[index],
                    "score": float(round(score, 4)),
                }
            )

        logger.debug("Semantic search returned %d result(s).", len(results))
        return results

    def save(self, save_dir: Path) -> None:
        """
        Saves the FAISS index and metadata to disk.

        Creates two files:
        - <save_dir>/faiss.index  — the FAISS binary index
        - <save_dir>/metadata.pkl — paragraphs and sources as a pickle file

        Args:
            save_dir: Directory path where index files will be written.
        """
        import faiss

        save_dir.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self._index, str(save_dir / "faiss.index"))

        with open(save_dir / "metadata.pkl", "wb") as f:
            pickle.dump(
                {"paragraphs": self._paragraphs, "sources": self._sources},
                f,
            )

        logger.info("Vector store saved to: %s", save_dir)

    def load(self, save_dir: Path) -> None:
        """
        Loads a previously saved FAISS index and metadata from disk.

        Args:
            save_dir: Directory path containing faiss.index and metadata.pkl.

        Raises:
            FileNotFoundError: If either index file is missing.
        """
        import faiss

        index_path = save_dir / "faiss.index"
        metadata_path = save_dir / "metadata.pkl"

        if not index_path.exists() or not metadata_path.exists():
            raise FileNotFoundError(
                f"Index files not found in: {save_dir}. "
                "Run the application once to build and save the index."
            )

        self._index = faiss.read_index(str(index_path))

        with open(metadata_path, "rb") as f:
            metadata = pickle.load(f)

        self._paragraphs = metadata["paragraphs"]
        self._sources = metadata["sources"]
        self._is_built = True

        logger.info(
            "Vector store loaded from: %s (%d vectors).",
            save_dir,
            len(self._paragraphs),
        )

    @property
    def size(self) -> int:
        """Returns the number of vectors stored in the index."""
        return len(self._paragraphs)

    @property
    def is_built(self) -> bool:
        """Returns True if the index has been built or loaded."""
        return self._is_built
