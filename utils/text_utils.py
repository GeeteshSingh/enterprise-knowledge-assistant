import pprint
def clean_query(query: str) -> list[str]:
   normalized = query.strip().lower().replace("?", "").replace(".", "").replace(",", "")
   words = normalized.split()
   stop_words = {"what", "is", "the", "are", "do", "to", "and", "a", "an"}   
   cleansed_words = [word for word in words if word not in stop_words]
   return cleansed_words

input_query = "What is Apache Kafka?"
output = clean_query(input_query)
print(output)

paragraphs = [
    "Apache Kafka is an event streaming platform.",
    "Spark processes big data.",
    "Apache Kafka integrates with Spark."
]

index = {}
for paragraph_index, text in enumerate(paragraphs):
    
    cleaned_words = clean_query(text)
    
    for word in cleaned_words:
        
        if word not in index:
            index[word] = [paragraph_index]
        else:
            if paragraph_index not in index[word]:
                index[word].append(paragraph_index)

print("--- Dynamic Keyword Index Completed ---")
print(index)
import pprint
pprint.pprint(index)


def search_document(keywords, index, paragraphs):
    results = []
    paragraph_numbers = index.get(keywords[0], [])

    for num in paragraph_numbers:
        results.append(paragraphs[num])
    return results

def get_unique_indices(keywords: list[str], index: dict[str, list[int]]) -> list[int]:
    matched_indices = set()
    
    for keyword in keywords:
        paragraph_indices = index.get(keyword, [])
        
        for num in paragraph_indices:
            matched_indices.add(num)
            
    return sorted(matched_indices)

keywords = ["apache", "kafka"]

matched_indices = get_unique_indices(keywords, index)

print("--- Unique Matching Paragraph Indices ---")
print(matched_indices)

results = []
for paragraph_index in matched_indices:
    results.append(paragraphs[paragraph_index])

print("\n--- Final Retrieved Paragraphs ---")
print(results)
# def clean_query(query: str) -> str:
#     query = query.strip().lower().replace("?", "")
#     words = query.split()
    
#     stop_words = {"what", "is", "the", "are", "do", "to", "and", "a", "an"}
    
#     cleansed_words = [word for word in words if word not in stop_words]
    
#     return " ".join(cleansed_words)

# input_query = "What is Apache Kafka?"
# output = clean_query(input_query)
# print(output) 