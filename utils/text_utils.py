from pathlib import Path


STOP_WORDS = {
    "what", "is", "the", "are", "do", "to", "and", "a", "an",
    "of", "in", "for", "on", "with", "at", "by", "from", "as",
    "was", "were", "be", "been", "being", "have", "has", "had",
    "does", "did", "will", "would", "could", "should", "may",
    "might", "shall", "can", "it", "its", "this", "that", "these",
    "those", "i", "me", "my", "we", "our", "you", "your", "he",
    "she", "they", "them", "their", "how", "which", "who", "or",
    "not", "but", "so", "if", "about", "into", "than", "then",
    "up", "out", "no", "any", "also",
}

PUNCTUATION_TO_REMOVE = str.maketrans("", "", "?.,!;:\"'()[]{}–-")


def clean_query(query: str) -> list[str]:
    """
    Normalizes a query string into a list of meaningful keywords.

    Steps:
    - Strip leading and trailing whitespace
    - Convert to lowercase
    - Remove punctuation characters
    - Split into words
    - Remove stop words

    Args:
        query: Raw user query or paragraph text.

    Returns:
        List of cleaned keyword strings.
    """
    normalized = query.strip().lower().translate(PUNCTUATION_TO_REMOVE)
    words = normalized.split()
    keywords = [word for word in words if word not in STOP_WORDS]
    return keywords


def build_index(paragraphs: list[str]) -> dict[str, list[int]]:
    """
    Builds an inverted keyword index from a list of paragraphs.

    The index maps each keyword to a sorted list of paragraph indices
    where that keyword appears.

    Args:
        paragraphs: List of paragraph strings to index.

    Returns:
        Dictionary mapping keyword -> list of paragraph indices.

    Example:
        {
            "apache": [0, 2],
            "kafka":  [0, 2],
            "spark":  [1, 2]
        }
    """
    index: dict[str, list[int]] = {}

    for paragraph_index, text in enumerate(paragraphs):
        keywords = clean_query(text)

        for keyword in keywords:
            if keyword not in index:
                index[keyword] = [paragraph_index]
            elif paragraph_index not in index[keyword]:
                index[keyword].append(paragraph_index)

    return index


def get_unique_indices(
    keywords: list[str],
    index: dict[str, list[int]],
    mode: str = "or",
) -> list[int]:
    """
    Looks up query keywords in the index and returns matching paragraph indices.

    Supports two retrieval modes:
    - "or"  : Returns paragraphs that contain ANY of the keywords (OR logic).
    - "and" : Returns only paragraphs that contain ALL of the keywords (AND logic).

    Args:
        keywords: List of query keywords to look up.
        index:    Inverted keyword index built by build_index().
        mode:     Retrieval mode, either "or" or "and". Defaults to "or".

    Returns:
        Sorted list of unique paragraph indices that match the query.
    """
    if not keywords:
        return []

    if mode == "and":
        # Start with all indices for the first keyword, then intersect
        first_keyword = keywords[0]
        matched_indices = set(index.get(first_keyword, []))

        for keyword in keywords[1:]:
            keyword_indices = set(index.get(keyword, []))
            matched_indices = matched_indices.intersection(keyword_indices)
    else:
        # OR mode: union of all keyword indices
        matched_indices: set[int] = set()

        for keyword in keywords:
            paragraph_indices = index.get(keyword, [])
            for paragraph_index in paragraph_indices:
                matched_indices.add(paragraph_index)

    return sorted(matched_indices)


def retrieve_paragraphs(
    paragraph_indices: list[int],
    paragraphs: list[str],
) -> list[str]:
    """
    Retrieves the original paragraph text for each given index.

    Args:
        paragraph_indices: List of paragraph indices to retrieve.
        paragraphs:        Original list of paragraph strings.

    Returns:
        List of paragraph strings corresponding to the given indices.
    """
    return [paragraphs[index] for index in paragraph_indices]


def score_paragraph(paragraph: str, keywords: list[str]) -> int:
    """
    Calculates a relevance score for a paragraph based on keyword matches.

    The score equals the number of query keywords that appear in the paragraph.
    A higher score means the paragraph is more relevant to the query.

    Args:
        paragraph: Paragraph text to score.
        keywords:  List of query keywords.

    Returns:
        Integer relevance score.
    """
    paragraph_keywords = set(clean_query(paragraph))
    return sum(1 for keyword in keywords if keyword in paragraph_keywords)


def chunk_document(content: str, chunk_size: int = 3, overlap: int = 1) -> list[str]:
    """
    Splits a document into overlapping chunks of paragraphs.

    This is useful for large documents where individual paragraphs may be
    too short to provide enough context for a search result.

    Args:
        content:    Full document text.
        chunk_size: Number of paragraphs per chunk. Defaults to 3.
        overlap:    Number of paragraphs to overlap between consecutive chunks.
                    Defaults to 1.

    Returns:
        List of chunk strings, where each chunk is a group of paragraphs
        joined by double newlines.
    """
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]

    if len(paragraphs) <= chunk_size:
        return ["\n\n".join(paragraphs)]

    chunks = []
    step = chunk_size - overlap
    index = 0

    while index < len(paragraphs):
        chunk = paragraphs[index: index + chunk_size]
        chunks.append("\n\n".join(chunk))
        index += step

    return chunks