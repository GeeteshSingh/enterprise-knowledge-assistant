import unittest
from pathlib import Path
import tempfile
import os

from utils.text_utils import (
    clean_query,
    build_index,
    get_unique_indices,
    retrieve_paragraphs,
    score_paragraph,
    chunk_document,
)
from utils.file_utils import load_document, load_all_documents, split_into_paragraphs


class TestCleanQuery(unittest.TestCase):
    """Tests for the clean_query function."""

    def test_converts_to_lowercase(self):
        result = clean_query("Apache Kafka")
        self.assertEqual(result, ["apache", "kafka"])

    def test_removes_question_mark(self):
        result = clean_query("What is Kafka?")
        self.assertNotIn("kafka?", result)
        self.assertIn("kafka", result)

    def test_removes_stop_words(self):
        result = clean_query("What is the best approach?")
        for stop_word in ["what", "is", "the"]:
            self.assertNotIn(stop_word, result)

    def test_removes_various_punctuation(self):
        result = clean_query("Kafka, Spark; and Python!")
        self.assertIn("kafka", result)
        self.assertIn("spark", result)
        self.assertIn("python", result)

    def test_handles_empty_string(self):
        result = clean_query("")
        self.assertEqual(result, [])

    def test_handles_only_stop_words(self):
        result = clean_query("what is the a an")
        self.assertEqual(result, [])

    def test_strips_whitespace(self):
        result = clean_query("   kafka   ")
        self.assertEqual(result, ["kafka"])

    def test_returns_list(self):
        result = clean_query("Kafka")
        self.assertIsInstance(result, list)


class TestBuildIndex(unittest.TestCase):
    """Tests for the build_index function."""

    def setUp(self):
        self.paragraphs = [
            "Apache Kafka is an event streaming platform.",
            "Spark processes big data efficiently.",
            "Apache Kafka integrates with Spark.",
        ]
        self.index = build_index(self.paragraphs)

    def test_returns_dict(self):
        self.assertIsInstance(self.index, dict)

    def test_kafka_appears_in_correct_paragraphs(self):
        self.assertIn("kafka", self.index)
        self.assertEqual(sorted(self.index["kafka"]), [0, 2])

    def test_spark_appears_in_correct_paragraphs(self):
        self.assertIn("spark", self.index)
        self.assertEqual(sorted(self.index["spark"]), [1, 2])

    def test_apache_appears_in_correct_paragraphs(self):
        self.assertIn("apache", self.index)
        self.assertEqual(sorted(self.index["apache"]), [0, 2])

    def test_no_duplicate_indices(self):
        for keyword, indices in self.index.items():
            self.assertEqual(len(indices), len(set(indices)), f"Duplicate indices for keyword: {keyword}")

    def test_empty_paragraphs_returns_empty_index(self):
        index = build_index([])
        self.assertEqual(index, {})


class TestGetUniqueIndices(unittest.TestCase):
    """Tests for the get_unique_indices function."""

    def setUp(self):
        self.index = {
            "apache": [0, 2],
            "kafka": [0, 2],
            "spark": [1, 2],
            "big": [1],
        }

    def test_or_mode_returns_union(self):
        result = get_unique_indices(["kafka", "spark"], self.index, mode="or")
        self.assertEqual(result, [0, 1, 2])

    def test_and_mode_returns_intersection(self):
        result = get_unique_indices(["apache", "spark"], self.index, mode="and")
        self.assertEqual(result, [2])

    def test_and_mode_no_intersection_returns_empty(self):
        result = get_unique_indices(["big", "kafka"], self.index, mode="and")
        self.assertEqual(result, [])

    def test_unknown_keyword_returns_no_results_in_and_mode(self):
        result = get_unique_indices(["kafka", "nonexistent"], self.index, mode="and")
        self.assertEqual(result, [])

    def test_unknown_keyword_is_ignored_in_or_mode(self):
        result = get_unique_indices(["kafka", "nonexistent"], self.index, mode="or")
        self.assertEqual(result, [0, 2])

    def test_returns_sorted_list(self):
        result = get_unique_indices(["spark", "apache"], self.index, mode="or")
        self.assertEqual(result, sorted(result))

    def test_empty_keywords_returns_empty(self):
        result = get_unique_indices([], self.index, mode="or")
        self.assertEqual(result, [])

    def test_default_mode_is_or(self):
        result_default = get_unique_indices(["kafka", "spark"], self.index)
        result_or = get_unique_indices(["kafka", "spark"], self.index, mode="or")
        self.assertEqual(result_default, result_or)


class TestRetrieveParagraphs(unittest.TestCase):
    """Tests for the retrieve_paragraphs function."""

    def setUp(self):
        self.paragraphs = [
            "Paragraph zero.",
            "Paragraph one.",
            "Paragraph two.",
        ]

    def test_retrieves_correct_paragraphs(self):
        result = retrieve_paragraphs([0, 2], self.paragraphs)
        self.assertEqual(result, ["Paragraph zero.", "Paragraph two."])

    def test_single_index(self):
        result = retrieve_paragraphs([1], self.paragraphs)
        self.assertEqual(result, ["Paragraph one."])

    def test_empty_indices_returns_empty_list(self):
        result = retrieve_paragraphs([], self.paragraphs)
        self.assertEqual(result, [])

    def test_returns_list(self):
        result = retrieve_paragraphs([0], self.paragraphs)
        self.assertIsInstance(result, list)


class TestScoreParagraph(unittest.TestCase):
    """Tests for the score_paragraph function."""

    def test_score_is_number_of_matching_keywords(self):
        paragraph = "Apache Kafka is an event streaming platform."
        score = score_paragraph(paragraph, ["apache", "kafka"])
        self.assertEqual(score, 2)

    def test_score_zero_when_no_keywords_match(self):
        paragraph = "Python is great for data science."
        score = score_paragraph(paragraph, ["kafka", "spark"])
        self.assertEqual(score, 0)

    def test_score_is_integer(self):
        paragraph = "Kafka processes events."
        score = score_paragraph(paragraph, ["kafka"])
        self.assertIsInstance(score, int)


class TestChunkDocument(unittest.TestCase):
    """Tests for the chunk_document function."""

    def setUp(self):
        self.content = "\n\n".join([
            "Paragraph one.",
            "Paragraph two.",
            "Paragraph three.",
            "Paragraph four.",
            "Paragraph five.",
        ])

    def test_returns_list(self):
        result = chunk_document(self.content, chunk_size=3)
        self.assertIsInstance(result, list)

    def test_small_document_returns_single_chunk(self):
        small_content = "Paragraph one.\n\nParagraph two."
        result = chunk_document(small_content, chunk_size=5)
        self.assertEqual(len(result), 1)

    def test_chunks_have_overlap(self):
        result = chunk_document(self.content, chunk_size=3, overlap=1)
        # With 5 paragraphs, chunk_size=3, overlap=1: step=2
        # Chunks: [0,1,2], [2,3,4] -> 2 chunks
        self.assertGreaterEqual(len(result), 2)

    def test_each_chunk_is_string(self):
        result = chunk_document(self.content, chunk_size=3)
        for chunk in result:
            self.assertIsInstance(chunk, str)


class TestLoadDocument(unittest.TestCase):
    """Tests for the load_document function in file_utils."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def test_loads_valid_file(self):
        file_path = Path(self.temp_dir) / "test.txt"
        file_path.write_text("Hello, world.", encoding="utf-8")
        result = load_document(file_path)
        self.assertEqual(result, "Hello, world.")

    def test_raises_file_not_found(self):
        file_path = Path(self.temp_dir) / "nonexistent.txt"
        with self.assertRaises(FileNotFoundError):
            load_document(file_path)

    def test_raises_value_error_for_empty_file(self):
        file_path = Path(self.temp_dir) / "empty.txt"
        file_path.write_text("", encoding="utf-8")
        with self.assertRaises(ValueError):
            load_document(file_path)

    def test_returns_string(self):
        file_path = Path(self.temp_dir) / "test2.txt"
        file_path.write_text("Some content.", encoding="utf-8")
        result = load_document(file_path)
        self.assertIsInstance(result, str)


class TestLoadAllDocuments(unittest.TestCase):
    """Tests for the load_all_documents function in file_utils."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def test_loads_multiple_txt_files(self):
        for i in range(3):
            file_path = Path(self.temp_dir) / f"doc{i}.txt"
            file_path.write_text(f"Content {i}.", encoding="utf-8")

        result = load_all_documents(Path(self.temp_dir))
        self.assertEqual(len(result), 3)

    def test_ignores_non_txt_files(self):
        Path(self.temp_dir, "doc.txt").write_text("Valid.", encoding="utf-8")
        Path(self.temp_dir, "doc.pdf").write_text("Should be ignored.", encoding="utf-8")
        result = load_all_documents(Path(self.temp_dir))
        self.assertEqual(len(result), 1)

    def test_returns_empty_dict_for_empty_directory(self):
        result = load_all_documents(Path(self.temp_dir))
        self.assertEqual(result, {})

    def test_raises_error_for_missing_directory(self):
        with self.assertRaises(FileNotFoundError):
            load_all_documents(Path(self.temp_dir) / "nonexistent")

    def test_returns_dict_with_filename_keys(self):
        Path(self.temp_dir, "myfile.txt").write_text("Hello.", encoding="utf-8")
        result = load_all_documents(Path(self.temp_dir))
        self.assertIn("myfile.txt", result)


class TestSplitIntoParagraphs(unittest.TestCase):
    """Tests for the split_into_paragraphs function."""

    def test_splits_on_double_newline(self):
        content = "First paragraph.\n\nSecond paragraph."
        result = split_into_paragraphs(content)
        self.assertEqual(len(result), 2)

    def test_removes_empty_paragraphs(self):
        content = "First.\n\n\n\nSecond."
        result = split_into_paragraphs(content)
        self.assertEqual(len(result), 2)

    def test_strips_whitespace_from_paragraphs(self):
        content = "  First.  \n\n  Second.  "
        result = split_into_paragraphs(content)
        self.assertEqual(result[0], "First.")
        self.assertEqual(result[1], "Second.")

    def test_single_paragraph_returns_list_of_one(self):
        content = "Only one paragraph."
        result = split_into_paragraphs(content)
        self.assertEqual(len(result), 1)

    def test_empty_string_returns_empty_list(self):
        result = split_into_paragraphs("")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
