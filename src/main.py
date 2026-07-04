# Open the file in read mode ('r')
def split_into_paragraphs(text):
    paragraphs = text.split("\n\n")  # Spliting by double newlines
    return [p.strip() for p in paragraphs if p.strip()]  # Removing empty paragraphs

file_location = "data/sample.txt"  # Specifying the path to my text file
words = ["Python", "is", "awesome"]

print(" ".join(words))
try:
    with open(file_location, "r") as file:
        content = file.read()
        if len(content) > 0:
            print("File Loaded Successfully")
            print(f"Total Characters: {len(content)}")
            line_count = len(content.splitlines())
            print(f"Total Lines: {line_count}")
            print(f"File Path: {file_location}")
            print("-" * 40)
            
            # Converting the single large string into a list of paragraphs
            paragraphs_list = split_into_paragraphs(content)
            
            # --- STEP 3: Ask the User ---
            user_query = input("Enter your question: ")
            print("-" * 40)
            
            # --- STEP 4: Searching Logic ---
            found = False
            for paragraph in paragraphs_list:
                # Basic case-sensitive check for today
                if user_query in paragraph:
                    print(paragraph)
                    print()  # Print a blank line for spacing
                    found = True
            
            if not found:
                print(f"No paragraphs found containing: '{user_query}'")
                
        else:
            print("File Not Loaded (File is empty)")

except FileNotFoundError:
    print(f"Error: The file at '{file_location}' could not be found.")
except PermissionError:
    print(f"Error: You do not have permission to read the file at '{file_location}'.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")




# from pathlib import Path


# def load_document(file_path: Path) -> str:
#     """
#     Reads the contents of a text file.

#     Args:
#         file_path: Path object representing the file location.

#     Returns:
#         File content as a string.
#     """
#     with file_path.open("r", encoding="utf-8") as file:
#         return file.read()


# def split_into_paragraphs(content: str) -> list[str]:
#     """
#     Splits document into paragraphs and removes empty entries.
#     """
#     return [paragraph.strip() for paragraph in content.split("\n\n") if paragraph.strip()]


# def search_document(paragraphs: list[str], query: str) -> list[str]:
#     """
#     Searches for paragraphs containing the user's query.

#     Returns:
#         List of matching paragraphs.
#     """
#     matches = []

#     for paragraph in paragraphs:
#         if query.lower() in paragraph.lower():
#             matches.append(paragraph)

#     return matches


# def print_summary(file_path: Path, content: str) -> None:
#     """
#     Displays basic information about the document.
#     """
#     print("\nFile loaded successfully")
#     print("-" * 40)
#     print(f"Characters : {len(content)}")
#     print(f"Lines      : {len(content.splitlines())}")
#     print(f"Path       : {file_path.resolve()}")
#     print("-" * 40)


# def main() -> None:

#     file_path = Path("data") / "sample.txt"

#     try:
#         content = load_document(file_path)

#         print_summary(file_path, content)

#         paragraphs = split_into_paragraphs(content)

#         query = input("Enter your question: ").strip()

#         results = search_document(paragraphs, query)

#         print("\nSearch Results")
#         print("-" * 40)

#         if results:
#             for result in results:
#                 print(result)
#                 print()

#         else:
#             print("No matching paragraph found.")

#     except FileNotFoundError:
#         print(f"ERROR: File not found -> {file_path}")

#     except PermissionError:
#         print(f"ERROR: Permission denied -> {file_path}")

#     except Exception as e:
#         print(f"Unexpected error: {e}")


# if __name__ == "__main__":
#     main()