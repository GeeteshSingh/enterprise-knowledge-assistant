import numpy as np

from utils.logger import get_logger


logger = get_logger(__name__)

MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingEngine:
    """
    Generates dense vector embeddings for text using a local sentence-transformers model.

    The model runs entirely on the local machine and does not require an API key
    or an internet connection after the initial model download.

    Model used: all-MiniLM-L6-v2
    - Embedding dimensions: 384
    - Fast inference, good general-purpose semantic quality
    - License: Apache 2.0
    """

    def __init__(self) -> None:
        self._model = None

    def _load_model(self) -> None:
        """
        Lazily loads the sentence-transformers model on first use.

        Importing sentence_transformers is deferred here so that the rest of
        the application can start without it if only keyword search is used.
        """
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            logger.info("Loading embedding model: %s", MODEL_NAME)
            self._model = SentenceTransformer(MODEL_NAME)
            logger.info("Embedding model loaded successfully.")

    def embed_texts(self, texts: list[str]) -> np.ndarray:
        """
        Generates embeddings for a list of text strings.

        Args:
            texts: List of strings to embed.

        Returns:
            NumPy array of shape (len(texts), embedding_dim) with float32 values.
        """
        self._load_model()
        logger.debug("Generating embeddings for %d text(s).", len(texts))
        embeddings = self._model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False,
            normalize_embeddings=True,
        )
        return embeddings.astype(np.float32)

    def embed_query(self, query: str) -> np.ndarray:
        """
        Generates an embedding for a single query string.

        Args:
            query: Query string to embed.

        Returns:
            NumPy array of shape (1, embedding_dim) with float32 values.
        """
        self._load_model()
        embedding = self._model.encode(
            [query],
            convert_to_numpy=True,
            show_progress_bar=False,
            normalize_embeddings=True,
        )
        return embedding.astype(np.float32)

    @property
    def embedding_dim(self) -> int:
        """Returns the number of dimensions in each embedding vector."""
        self._load_model()
        return self._model.get_sentence_embedding_dimension()
