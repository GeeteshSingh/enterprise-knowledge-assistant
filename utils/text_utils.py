import pprint


def clean_query(query: str) -> list[str]:
    normalized = (
        query.strip()
        .lower()
        .replace("?", "")
        .replace(".", "")
        .replace(",", "")
    )

    words = normalized.split()

    stop_words = {
        "what",
        "is",
        "the",
        "are",
        "do",
        "to",
        "and",
        "a",
        "an",
    }

    cleansed_words = [
        word for word in words
        if word not in stop_words
    ]

    return cleansed_words


def build_index(
    paragraphs: list[str],
) -> dict[str, list[int]]:
    index = {}

    for paragraph_index, text in enumerate(paragraphs):
        cleaned_words = clean_query(text)

        for word in cleaned_words:
            if word not in index:
                index[word] = [paragraph_index]
            elif paragraph_index not in index[word]:
                index[word].append(paragraph_index)

    return index


def get_unique_indices(
    keywords: list[str],
    index: dict[str, list[int]],
) -> list[int]:
    matched_indices = set()

    for keyword in keywords:
        paragraph_indices = index.get(keyword, [])

        for paragraph_index in paragraph_indices:
            matched_indices.add(paragraph_index)

    return sorted(matched_indices)


def retrieve_paragraphs(
    paragraph_indices: list[int],
    paragraphs: list[str],
) -> list[str]:
    results = []

    for paragraph_index in paragraph_indices:
        results.append(paragraphs[paragraph_index])

    return results


paragraphs = [
    "Apache Kafka is an event streaming platform.",
    "Spark processes big data.",
    "Apache Kafka integrates with Spark.",
]

input_query = "What is Apache Kafka?"

keywords = clean_query(input_query)

index = build_index(paragraphs)

matched_indices = get_unique_indices(
    keywords,
    index,
)

results = retrieve_paragraphs(
    matched_indices,
    paragraphs,
)


print("--- Cleaned Keywords ---")
print(keywords)

print("\n--- Dynamic Keyword Index Completed ---")
pprint.pprint(index)

print("\n--- Unique Matching Paragraph Indices ---")
print(matched_indices)

print("\n--- Search Results ---")

for result in results:
    print(result)
    print()