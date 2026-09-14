from pathlib import Path

from utils.file_utils import load_all_documents, split_into_paragraphs
from utils.logger import get_logger
from utils.text_utils import (
    build_index,
    clean_query,
    get_unique_indices,
    retrieve_paragraphs,
    score_paragraph,
)


logger = get_logger(__name__)


class SearchResult:
    """
    Represents a single search result.

    Attributes:
        paragraph: The matching paragraph text.
        source:    The filename the paragraph came from.
        score:     Relevance score (number of matching keywords).
    """

    def __init__(self, paragraph: str, source: str, score: int) -> None:
        self.paragraph = paragraph
        self.source = source
        self.score = score

    def __repr__(self) -> str:
        return f"SearchResult(source={self.source!r}, score={self.score}, paragraph={self.paragraph[:60]!r})"


class SearchEngine:
    """
    A keyword-based document search engine.

    Workflow:
    1. load_documents() — reads all .txt files from the data directory.
    2. build()          — splits documents into paragraphs and builds the
                         inverted keyword index.
    3. search()         — accepts a user query, cleans it, looks up the
                         index, scores results, and returns ranked matches.

    Supports two search modes:
    - "or"  : Returns paragraphs containing ANY query keyword (default).
    - "and" : Returns paragraphs containing ALL query keywords.
    """

    def __init__(self, data_dir: Path) -> None:
        """
        Args:
            data_dir: Path to the directory containing .txt document files.
        """
        self._data_dir = data_dir
        self._documents: dict[str, str] = {}
        self._paragraphs: list[str] = []
        self._paragraph_sources: list[str] = []
        self._index: dict[str, list[int]] = {}
        self._is_built = False

    def load_documents(self) -> None:
        """
        Loads all .txt files from the data directory.

        Logs the number of documents loaded and their filenames.
        """
        logger.info("Loading documents from: %s", self._data_dir)
        self._documents = load_all_documents(self._data_dir)

        if not self._documents:
            logger.warning("No documents found in: %s", self._data_dir)
        else:
            logger.info("Loaded %d document(s): %s", len(self._documents), list(self._documents.keys()))

    def build(self) -> None:
        """
        Splits all loaded documents into paragraphs and builds the inverted index.

        Each paragraph is tracked with its source filename so search results
        can display where the match came from.

        Must be called after load_documents().
        """
        logger.info("Building keyword index...")
        self._paragraphs = []
        self._paragraph_sources = []

        for filename, content in self._documents.items():
            paragraphs = split_into_paragraphs(content)
            for paragraph in paragraphs:
                self._paragraphs.append(paragraph)
                self._paragraph_sources.append(filename)

        self._index = build_index(self._paragraphs)
        self._is_built = True

        logger.info(
            "Index built: %d paragraph(s) indexed across %d document(s). %d unique keyword(s).",
            len(self._paragraphs),
            len(self._documents),
            len(self._index),
        )

    def search(self, query: str, mode: str = "or") -> list[SearchResult]:
        """
        Searches the index for paragraphs matching the query.

        Steps:
        1. Cleans the query into keywords.
        2. Looks up matching paragraph indices from the index.
        3. Retrieves the matching paragraph texts.
        4. Scores each paragraph by counting matching keywords.
        5. Sorts results by score (highest first).

        Args:
            query: Raw user query string.
            mode:  "or" returns paragraphs matching ANY keyword.
                   "and" returns paragraphs matching ALL keywords.

        Returns:
            List of SearchResult objects sorted by relevance score, highest first.
            Returns an empty list if no matches are found or the engine has not
            been built yet.
        """
        if not self._is_built:
            logger.error("Search engine has not been built. Call build() first.")
            return []

        logger.debug("Searching for query: %r (mode=%s)", query, mode)

        keywords = clean_query(query)
        logger.debug("Cleaned keywords: %s", keywords)

        if not keywords:
            logger.warning("Query produced no keywords after cleaning: %r", query)
            return []

        matched_indices = get_unique_indices(keywords, self._index, mode=mode)
        logger.debug("Matched paragraph indices: %s", matched_indices)

        if not matched_indices:
            logger.info("No results found for query: %r", query)
            return []

        matched_paragraphs = retrieve_paragraphs(matched_indices, self._paragraphs)

        results = []
        for index, paragraph in zip(matched_indices, matched_paragraphs):
            source = self._paragraph_sources[index]
            score = score_paragraph(paragraph, keywords)
            results.append(SearchResult(paragraph=paragraph, source=source, score=score))

        # Sort by score descending so the most relevant result appears first
        results.sort(key=lambda result: result.score, reverse=True)

        logger.info("Found %d result(s) for query: %r", len(results), query)
        return results

    @property
    def document_count(self) -> int:
        """Returns the number of loaded documents."""
        return len(self._documents)

    @property
    def paragraph_count(self) -> int:
        """Returns the total number of indexed paragraphs."""
        return len(self._paragraphs)

    @property
    def keyword_count(self) -> int:
        """Returns the number of unique keywords in the index."""
        return len(self._index)
