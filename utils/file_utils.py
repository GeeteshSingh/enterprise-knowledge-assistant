from pathlib import Path


def load_document(file_path: Path) -> str:
    """
    Reads the full text content of a single file.

    Args:
        file_path: Path object pointing to the text file.

    Returns:
        File content as a single string.

    Raises:
        FileNotFoundError: If the file does not exist at the given path.
        PermissionError:   If the process lacks read permission for the file.
        ValueError:        If the file exists but contains no content.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as file:
        content = file.read()

    if not content.strip():
        raise ValueError(f"File is empty: {file_path}")

    return content


def load_all_documents(data_dir: Path) -> dict[str, str]:
    """
    Reads all .txt files from a directory and returns their contents.

    Each file is loaded using load_document(). Files that raise an error
    are skipped and the error is printed to stdout.

    Args:
        data_dir: Path object pointing to the directory containing text files.

    Returns:
        Dictionary mapping filename (str) -> file content (str).
        Returns an empty dict if the directory contains no .txt files.

    Raises:
        FileNotFoundError: If the directory itself does not exist.
    """
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    documents: dict[str, str] = {}

    txt_files = sorted(data_dir.glob("*.txt"))

    if not txt_files:
        return documents

    for file_path in txt_files:
        try:
            content = load_document(file_path)
            documents[file_path.name] = content
        except (ValueError, PermissionError) as error:
            print(f"Skipping {file_path.name}: {error}")

    return documents


def split_into_paragraphs(content: str) -> list[str]:
    """
    Splits a document string into a list of non-empty paragraphs.

    Paragraphs are separated by double newlines. Empty paragraphs
    resulting from the split are removed.

    Args:
        content: Full document text as a single string.

    Returns:
        List of paragraph strings with leading/trailing whitespace stripped.
    """
    return [p.strip() for p in content.split("\n\n") if p.strip()]
