from pathlib import Path

from config.settings import settings
from src.rag_pipeline import RAGPipeline
from src.search_engine import SearchEngine
from utils.logger import get_logger


logger = get_logger(__name__)

SEPARATOR = "-" * 60


def display_keyword_result(index: int, result) -> None:
    """
    Prints a single keyword search result.

    Args:
        index:  1-based position in the ranked list.
        result: SearchResult object.
    """
    print(f"\nResult {index} | Source: {result.source} | Score: {result.score}")
    print(SEPARATOR)
    print(result.paragraph)


def display_semantic_result(index: int, result: dict) -> None:
    """
    Prints a single semantic search result.

    Args:
        index:  1-based position in the ranked list.
        result: Dict with 'paragraph', 'source', and 'score' keys.
    """
    print(f"\nResult {index} | Source: {result['source']} | Similarity: {result['score']:.4f}")
    print(SEPARATOR)
    print(result["paragraph"])


def run_keyword_session(engine: SearchEngine) -> None:
    """
    Runs an interactive keyword search session.

    Args:
        engine: A fully built SearchEngine instance.
    """
    print("\nKeyword Search Mode")
    print("Type your query. Append '| and' to use AND mode.")
    print("Example: Apache Kafka | and")
    print("Type 'back' to return to the main menu.")
    print(SEPARATOR)

    while True:
        raw_input = input("\nQuery: ").strip()

        if not raw_input:
            print("Query cannot be empty.")
            continue

        if raw_input.lower() == "back":
            break

        if "|" in raw_input:
            parts = raw_input.split("|", maxsplit=1)
            query = parts[0].strip()
            mode = parts[1].strip().lower()
            if mode not in {"or", "and"}:
                print(f"Unknown mode '{mode}'. Using 'or'.")
                mode = "or"
        else:
            query = raw_input
            mode = "or"

        logger.info("Keyword search: %r (mode=%s)", query, mode)
        results = engine.search(query, mode=mode)

        print(f"\nMode: {mode.upper()} | Query: {query}")
        print(SEPARATOR)

        if not results:
            print("No matching paragraphs found.")
        else:
            print(f"Found {len(results)} result(s), ranked by relevance:")
            for position, result in enumerate(results, start=1):
                display_keyword_result(position, result)

        print(SEPARATOR)


def run_semantic_session(rag: RAGPipeline) -> None:
    """
    Runs an interactive semantic search session.

    Args:
        rag: A fully built RAGPipeline instance.
    """
    print("\nSemantic Search Mode")
    print("Type your query to find semantically similar paragraphs.")
    print("Type 'back' to return to the main menu.")
    print(SEPARATOR)

    while True:
        query = input("\nQuery: ").strip()

        if not query:
            print("Query cannot be empty.")
            continue

        if query.lower() == "back":
            break

        logger.info("Semantic search: %r", query)
        results = rag.semantic_search(query, top_k=settings.TOP_K)

        print(f"\nQuery: {query}")
        print(SEPARATOR)

        if not results:
            print("No semantically similar paragraphs found.")
        else:
            print(f"Found {len(results)} result(s), ranked by similarity:")
            for position, result in enumerate(results, start=1):
                display_semantic_result(position, result)

        print(SEPARATOR)


def run_rag_session(rag: RAGPipeline) -> None:
    """
    Runs an interactive RAG question-answering session.

    Requires GEMINI_API_KEY to be configured. If not set, the user
    is informed and returned to the main menu.

    Args:
        rag: A fully built RAGPipeline instance.
    """
    if not settings.llm_available:
        print(
            "\nLLM features are not available.\n"
            "Set GEMINI_API_KEY in your .env file to enable answer generation.\n"
            "See .env.example for the required format."
        )
        return

    print("\nRAG Question Answering Mode")
    print("Ask a question. The assistant will retrieve context and generate an answer.")
    print("Type 'back' to return to the main menu.")
    print(SEPARATOR)

    while True:
        question = input("\nQuestion: ").strip()

        if not question:
            print("Question cannot be empty.")
            continue

        if question.lower() == "back":
            break

        logger.info("RAG query: %r", question)

        try:
            result = rag.query(question, top_k=settings.TOP_K)
        except (ValueError, RuntimeError) as error:
            print(f"\nError: {error}")
            continue

        print(f"\nQuestion: {question}")
        print(SEPARATOR)
        print("Answer:")
        print(result["answer"])
        print(SEPARATOR)
        print("Sources used:")
        for item in result["sources"]:
            print(f"  - [{item['source']}] {item['paragraph'][:80]}...")
        print(SEPARATOR)


def print_main_menu(keyword_engine: SearchEngine, rag: RAGPipeline) -> None:
    """Prints the main search mode selection menu."""
    print("\nEnterprise Knowledge Assistant")
    print(SEPARATOR)
    print(f"Documents loaded     : {keyword_engine.document_count}")
    print(f"Paragraphs indexed   : {keyword_engine.paragraph_count}")
    print(f"Unique keywords      : {keyword_engine.keyword_count}")
    print(f"Semantic index size  : {rag.vector_store_size}")
    print(f"LLM available        : {'Yes' if settings.llm_available else 'No (set GEMINI_API_KEY in .env)'}")
    print(SEPARATOR)
    print("Select search mode:")
    print("  1. Keyword Search")
    print("  2. Semantic Search")
    print("  3. Ask a Question (RAG)")
    print("  q. Quit")
    print(SEPARATOR)


def main() -> None:
    """
    Entry point for the Enterprise Knowledge Assistant CLI.

    Initializes both the keyword search engine and the RAG pipeline,
    then runs an interactive mode-selection menu.
    """
    logger.info("Starting Enterprise Knowledge Assistant.")

    keyword_engine = SearchEngine(data_dir=settings.data_path)
    rag_pipeline = RAGPipeline(data_dir=settings.data_path)

    try:
        keyword_engine.load_documents()
        keyword_engine.build()
    except FileNotFoundError as error:
        logger.error("Could not load documents for keyword engine: %s", error)
        print(f"Error: {error}")
        return

    try:
        rag_pipeline.build()
    except Exception as error:
        logger.error("Could not build RAG pipeline: %s", error)
        print(f"Warning: Semantic search unavailable — {error}")

    while True:
        print_main_menu(keyword_engine, rag_pipeline)
        choice = input("Enter choice: ").strip().lower()

        if choice == "1":
            run_keyword_session(keyword_engine)
        elif choice == "2":
            run_semantic_session(rag_pipeline)
        elif choice == "3":
            run_rag_session(rag_pipeline)
        elif choice in {"q", "quit", "exit"}:
            print("Exiting. Goodbye.")
            logger.info("User exited the application.")
            break
        else:
            print(f"Invalid choice: '{choice}'. Please enter 1, 2, 3, or q.")

    logger.info("Enterprise Knowledge Assistant stopped.")


if __name__ == "__main__":
    main()