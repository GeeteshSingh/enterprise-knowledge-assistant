# Enterprise Knowledge Assistant

> 🚀 A production-oriented AI Data Engineering project that evolves from basic document processing into a Retrieval-Augmented Generation (RAG) application using modern AI technologies.

---

## 📌 Project Status

**Current Phase:** Phase 3 — Search Engine Foundations

**Progress:** Day 6 / 90

### Current Capabilities

- ✅ Read text documents
- ✅ Display document summaries
- ✅ Split documents into paragraphs
- ✅ Normalize and clean user queries
- ✅ Remove common stop words
- ✅ Build an inverted keyword index
- ✅ Perform multi-keyword search
- ✅ Remove duplicate search results
- ✅ Retrieve matching paragraphs
- ✅ Maintain predictable document order
- ✅ Use modular and reusable search functions
- ✅ Handle common file-related exceptions

---

## 📖 Overview

Enterprise organizations store large amounts of information across documents such as PDFs, Word files, standard operating procedures, emails, reports, and internal knowledge bases.

Finding relevant information across these sources can be slow and difficult. This project demonstrates how to build an AI-powered Enterprise Knowledge Assistant capable of ingesting enterprise documents, retrieving relevant information, and eventually answering user questions using Retrieval-Augmented Generation (RAG).

Unlike tutorial-based projects, this application is being developed incrementally from the ground up. Each feature is implemented only after understanding the underlying Python concepts, software-engineering principles, design decisions, and trade-offs.

---

# 🏛 Current Architecture

```text
                  User
                    │
                    ▼
        "What is Apache Kafka?"
                    │
                    ▼
             clean_query()
                    │
                    ▼
          ["apache", "kafka"]
                    │
                    ▼
              build_index()
                    │
                    ▼
     Keyword → Paragraph Indices
                    │
                    ▼
         get_unique_indices()
                    │
                    ▼
                 [0, 2]
                    │
                    ▼
         retrieve_paragraphs()
                    │
                    ▼
        Matching Paragraph Text
                    │
                    ▼
                 Response
```

---

# 🎯 Project Goals

- Learn AI Data Engineering through hands-on development
- Strengthen Python fundamentals
- Build production-oriented Python applications
- Understand information retrieval and search systems
- Implement Retrieval-Augmented Generation (RAG)
- Work with embeddings and vector databases
- Integrate Large Language Models
- Build REST APIs using FastAPI
- Containerize applications using Docker
- Add automated testing and CI/CD
- Deploy applications to the cloud
- Follow software-engineering best practices

---

# 🛠 Technology Stack

## Current

- Python 3.x
- Git
- GitHub

## Planned

- Pytest
- Logging
- FastAPI
- Docker
- OpenAI API
- Gemini API
- FAISS
- LangChain
- LangGraph
- Vector Database
- GitHub Actions
- Cloud Platform

---

# 📂 Project Structure

```text
enterprise-knowledge-assistant/
│
├── data/
│   └── sample.txt
│
├── src/
│   └── main.py
│
├── utils/
│   └── text_utils.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🚀 Features

## Completed

- Text-file reading
- Character counting
- Line counting
- Document summaries
- File-related exception handling
- Paragraph splitting
- Query normalization
- Stop-word removal
- Keyword extraction
- Inverted keyword indexing
- Safe dictionary lookup
- Multi-keyword retrieval
- Duplicate-result removal
- Predictable result ordering
- Index-based paragraph retrieval
- Modular search functions
- Type hints

## Planned

- Connect the complete search pipeline to document files
- Read and process multiple documents
- Improve punctuation handling
- Add AND-based search
- Add relevance scoring
- Add result ranking
- Add semantic search
- Generate embeddings
- Integrate a vector database
- Build a RAG pipeline
- Integrate an LLM
- Build REST APIs using FastAPI
- Add automated testing
- Add application logging
- Containerize using Docker
- Add CI/CD
- Deploy to the cloud

---

# 🗺 Project Roadmap

## Phase 1 — Python Foundations

- [x] Project setup
- [x] File handling
- [x] Exception handling
- [x] Character counting
- [x] Line counting
- [x] Functions
- [x] Type hints
- [x] Introduction to `pathlib`
- [ ] Logging
- [ ] Unit testing

---

## Phase 2 — Document Processing

- [x] Paragraph splitting
- [x] Query preprocessing
- [x] Basic text cleaning
- [x] Stop-word removal
- [ ] Connect the search pipeline to document files
- [ ] Read multiple documents
- [ ] Improve text normalization
- [ ] Document chunking
- [ ] Metadata extraction

---

## Phase 3 — Search Engine

- [x] Basic keyword search
- [x] Inverted keyword indexing
- [x] Safe index lookup
- [x] Multi-keyword retrieval
- [x] Duplicate-result handling
- [x] Predictable result ordering
- [x] Paragraph retrieval
- [x] Modular search pipeline
- [ ] AND-based search
- [ ] Match scoring
- [ ] Result ranking
- [ ] Search relevance improvements

---

## Phase 4 — AI Integration

- [ ] Embeddings
- [ ] Vector database
- [ ] Semantic search
- [ ] Retrieval-Augmented Generation
- [ ] LLM integration
- [ ] Source-aware answers

---

## Phase 5 — Production Engineering

- [ ] FastAPI
- [ ] Configuration management
- [ ] Logging
- [ ] Unit testing
- [ ] Docker
- [ ] CI/CD
- [ ] Cloud deployment
- [ ] Monitoring

---

# 📅 Development Journal

## ✅ Day 1 — Text File Reader

### Objective

Build a safe text-file reader and display basic document information.

### Features Implemented

- Initialized the project repository
- Added a sample text document
- Read text content from a file
- Counted total characters
- Counted total lines
- Displayed the file path
- Added exception handling

### Python Concepts Learned

- File handling
- `with` statement
- `try-except`
- Functions
- Type hints
- Docstrings
- Introduction to `pathlib`

### Key Learning

A file should be opened safely and closed automatically using the `with` statement.

### Commit

```text
feat: add text file reader and document summary
```

---

## ✅ Day 2 — Keyword-Based Document Search

### Objective

Build a basic search system capable of finding relevant paragraphs without using AI.

### Features Implemented

- Split document content into paragraphs
- Stored paragraphs in a Python list
- Accepted user queries using `input()`
- Searched paragraphs using keywords
- Returned matching paragraphs
- Displayed a message when no results were found

### Python Concepts Learned

- Lists
- Loops
- Functions
- String methods
- User input
- List comprehensions
- Boolean flags

### Key Learning

Large document strings can be divided into smaller paragraphs to make retrieval easier.

### Commit

```text
feat: implement keyword-based document search
```

---

## ✅ Day 3 — Query Preprocessing

### Objective

Improve search behavior by cleaning and normalizing user queries.

### Features Implemented

- Created `clean_query()`
- Converted queries to lowercase
- Removed selected punctuation
- Split queries into words
- Removed common stop words
- Created a reusable text utility module

### Python Concepts Learned

- `strip()`
- `lower()`
- `replace()`
- `split()`
- `join()`
- String iteration
- List comprehensions
- Sets
- Return statements

### Key Learning

The position of a `return` statement changes program flow. A `return` placed inside a loop may end the function during the first iteration.

### Commit

```text
feat: add query preprocessing and text utility functions
```

---

## ✅ Day 4 — Building an Inverted Keyword Index

### Objective

Build an inverted keyword index to avoid scanning every paragraph for every search query.

### Features Implemented

- Updated `clean_query()` to return a list of keywords
- Used a set for efficient stop-word lookup
- Built an inverted index using a Python dictionary
- Stored keywords as dictionary keys
- Stored paragraph indices as dictionary values
- Prevented duplicate paragraph indices for repeated words

### Example

```python
{
    "apache": [0, 2],
    "kafka": [0, 2],
    "spark": [1, 2]
}
```

### Python Concepts Learned

- Dictionaries
- Sets
- `enumerate()`
- Nested loops
- Dictionary updates
- List `append()`
- List indexing

### Software-Engineering Concepts

- Inverted indexing
- Data modelling
- Algorithm design
- Code reusability

### Key Learning

An inverted index stores:

```text
Keyword
    ↓
Matching Paragraph Indices
```

Example:

```text
kafka → [0, 2]
```

This allows the application to locate relevant paragraphs directly instead of scanning the entire document for every query.

### Commit

```text
feat: build keyword index using dictionaries
```

---

## ✅ Day 5 — Multi-Keyword Search and Document Retrieval

### Objective

Use the inverted keyword index to retrieve relevant paragraphs for multiple query keywords.

### Features Implemented

- Added multi-keyword index lookup
- Used `dict.get()` for safe dictionary access
- Retrieved paragraph indices for every query keyword
- Used a set to remove duplicate paragraph indices
- Used `sorted()` to maintain predictable document order
- Retrieved original paragraph content using matching indices

### Search Flow

```text
User Query
    │
    ▼
"What is Apache Kafka?"
    │
    ▼
clean_query()
    │
    ▼
["apache", "kafka"]
    │
    ├── apache → [0, 2]
    │
    └── kafka  → [0, 2]
    │
    ▼
Combine Matching Indices
    │
    ▼
{0, 2}
    │
    ▼
Remove Duplicates and Sort
    │
    ▼
[0, 2]
    │
    ▼
Retrieve Original Paragraphs
    │
    ▼
Relevant Search Results
```

### Python Concepts Learned

- `dict.get()`
- Sets
- `set.add()`
- Nested loops
- List indexing
- List `append()`
- `sorted()`
- Function return values
- Data-type transformations

### Software-Engineering Concepts

- Safe dictionary lookup
- Defensive programming
- Multi-keyword retrieval
- Duplicate-result handling
- Deterministic result ordering
- Index-based document retrieval

### Key Learning

When multiple keywords point to the same paragraph, a set can remove duplicate paragraph indices.

Example:

```text
apache → [0, 2]

kafka → [0, 2]

Combined set → {0, 2}

Sorted result → [0, 2]
```

### Current Search Behavior

The current implementation uses **OR-based retrieval**.

For:

```text
Apache Kafka
```

a paragraph is returned when it contains:

```text
Apache OR Kafka
```

Future improvements will include AND-based retrieval, relevance scoring, and result ranking.

### Commit

```text
feat: implement multi-keyword document retrieval
```

---

## ✅ Day 6 — Refactoring the Keyword Search Pipeline

### Objective

Refactor the existing keyword-search logic into small, reusable functions with clear responsibilities.

The goal was to improve readability, maintainability, reusability, and testability without changing the existing search behavior.

### Improvements Implemented

- Moved keyword-index creation into `build_index()`
- Added `get_unique_indices()` for multi-keyword index lookup
- Used a set to remove duplicate paragraph indices
- Used `sorted()` to maintain predictable document order
- Added `retrieve_paragraphs()` to retrieve original paragraph text
- Removed the outdated single-keyword search implementation
- Removed duplicate imports and unnecessary function calls
- Connected the cleaned user query directly to the search pipeline
- Added type hints to search functions
- Improved variable names and code readability

### Current Search Pipeline

```text
User Query
    │
    ▼
"What is Apache Kafka?"
    │
    ▼
clean_query()
    │
    ▼
["apache", "kafka"]
    │
    ▼
build_index()
    │
    ▼
{
    "apache": [0, 2],
    "kafka": [0, 2],
    "spark": [1, 2]
}
    │
    ▼
get_unique_indices()
    │
    ▼
[0, 2]
    │
    ▼
retrieve_paragraphs()
    │
    ▼
Matching Paragraphs
```

### Functions Created

#### `clean_query()`

Normalizes text, removes selected punctuation and stop words, and returns meaningful keywords.

```python
def clean_query(
    query: str
) -> list[str]:
```

Example:

```text
Input:
"What is Apache Kafka?"

Output:
["apache", "kafka"]
```

#### `build_index()`

Processes all paragraphs and creates an inverted keyword index.

```python
def build_index(
    paragraphs: list[str]
) -> dict[str, list[int]]:
```

Example:

```python
{
    "apache": [0, 2],
    "kafka": [0, 2],
    "spark": [1, 2]
}
```

#### `get_unique_indices()`

Looks up all query keywords and returns unique matching paragraph indices in sorted order.

```python
def get_unique_indices(
    keywords: list[str],
    index: dict[str, list[int]]
) -> list[int]:
```

Example:

```text
Input:
["apache", "kafka"]

Output:
[0, 2]
```

#### `retrieve_paragraphs()`

Uses matching paragraph indices to retrieve the original paragraph text.

```python
def retrieve_paragraphs(
    paragraph_indices: list[int],
    paragraphs: list[str]
) -> list[str]:
```

Example output:

```text
Apache Kafka is an event streaming platform.

Apache Kafka integrates with Spark.
```

### Python Concepts Learned

- Function decomposition
- Function parameters
- Function return values
- Type hints
- Dictionaries
- Sets
- Nested loops
- `enumerate()`
- `dict.get()`
- `set.add()`
- `sorted()`
- List indexing
- List `append()`

### Software-Engineering Concepts

- Separation of Concerns
- Single Responsibility Principle
- Modular design
- Code reusability
- Readability
- Maintainability
- Refactoring without changing behavior

### Key Learning

A working application should not remain one large block of code.

Each function should have one clear responsibility:

```text
clean_query()
    → Clean and normalize text

build_index()
    → Build the inverted keyword index

get_unique_indices()
    → Find unique matching paragraph locations

retrieve_paragraphs()
    → Retrieve original paragraph content
```

Breaking the search pipeline into smaller functions makes the code easier to understand, test, debug, reuse, and extend.

### Commit

```text
refactor: modularize keyword search pipeline
```

---

# 🏗 Engineering Principles

This project follows:

- Clean Code
- Single Responsibility Principle
- Separation of Concerns
- Modular Design
- Reusable Functions
- Type Safety
- Defensive Programming
- Incremental Development
- Production-Oriented Engineering

---

# 📚 Learning Philosophy

This project is intentionally being built one feature at a time instead of copying a complete tutorial application.

Every feature is implemented only after understanding:

- Why it is required
- What problem it solves
- How the data moves through the application
- How the implementation works
- What trade-offs are involved
- How it fits into the overall architecture
- How the design can be improved for production use

---

# 📈 Current Progress

```text
███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 7%
```

## Current Milestones

- ✅ Python foundations
- ✅ Basic document processing
- ✅ Indexed keyword search
- ✅ Multi-keyword retrieval
- ✅ Modular search pipeline
- ⬜ File-connected search pipeline
- ⬜ Smarter search and ranking
- ⬜ Semantic search
- ⬜ Embeddings
- ⬜ Vector database
- ⬜ RAG
- ⬜ FastAPI
- ⬜ Docker
- ⬜ Cloud deployment

---

# 👨‍💻 Author

**Geetesh Singh**

Data Engineer transitioning into AI Data Engineering by building production-oriented projects from the ground up.

---

# 📄 License

This repository is intended for learning, portfolio development, and demonstration purposes.