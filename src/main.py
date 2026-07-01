# Open the file in read mode ('r')
file_location = "data/sample.txt"

try:
    with open(file_location, "r") as file:
        content = file.read()
        if len(content) > 0:
            print("File Loaded Successfully")
            print(f"Total Characters: {len(content)}")
            line_count = len(content.splitlines())
            print(f"Total Lines: {line_count}")
            print(f"File Path: {file_location}")
        else:
            print("File Not Loaded")

except FileNotFoundError:
    print(f"Error: The file at '{file_location}' could not be found.")
except PermissionError:
    print(f"Error: You do not have permission to read the file at '{file_location}'.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")




# from pathlib import Path


# def load_document(file_path: Path) -> str:
#     """
#     Reads and returns the contents of a text file.
#     Raises an exception if the file cannot be read.
#     """
#     with file_path.open("r", encoding="utf-8") as file:
#         return file.read()


# def print_summary(file_path: Path, content: str) -> None:
#     """
#     Prints a summary of the loaded document.
#     """
#     print("File loaded successfully")
#     print(f"Total Characters : {len(content)}")
#     print(f"Total Lines      : {len(content.splitlines())}")
#     print(f"File Path        : {file_path.resolve()}")


# def main() -> None:
#     file_path = Path("data") / "sample.txt"

#     try:
#         content = load_document(file_path)
#         print_summary(file_path, content)

#     except FileNotFoundError:
#         print(f"ERROR: File not found -> {file_path}")

#     except PermissionError:
#         print(f"ERROR: Permission denied -> {file_path}")

#     except Exception as e:
#         print(f"Unexpected error: {e}")


# if __name__ == "__main__":
#     main()