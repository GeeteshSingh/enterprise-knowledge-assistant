def clean_query(query: str) -> str:
   query = query.strip().lower().replace("?", "")
   words = query.split()
   stop_words = ["what", "is", "the", "are", "do", "to", "and", "a", "an"]
   cleansed_words = []
   for word in words:
        if word.lower() not in stop_words:
            if words.index(word) == 0:
                cleansed_words.append(word.lower())
            else:
                cleansed_words.append(word)
   return " ".join(cleansed_words)

input_query = "What is Apache Kafka?"
output = clean_query(input_query)
print(output)
# def clean_query(query: str) -> str:
#     query = query.strip().lower().replace("?", "")
#     words = query.split()
    
#     stop_words = {"what", "is", "the", "are", "do", "to", "and", "a", "an"}
    
#     cleansed_words = [word for word in words if word not in stop_words]
    
#     return " ".join(cleansed_words)

# input_query = "What is Apache Kafka?"
# output = clean_query(input_query)
# print(output) 