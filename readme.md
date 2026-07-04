# Enterprise Knowledge Assistant

> A production-oriented AI Data Engineering project that evolves from basic document processing into a Retrieval-Augmented Generation (RAG) application.

---

## 📖 Overview

Enterprise organizations store large amounts of information across documents, reports, SOPs, emails, and knowledge bases. Retrieving the right information quickly is often challenging.

This project demonstrates how to build an **AI-powered Enterprise Knowledge Assistant** capable of processing enterprise documents and answering user questions using modern AI technologies.

Unlike tutorial-based projects, this repository follows **production engineering practices**, with the application built incrementally from the ground up.

---

## 🎯 Goals

- Learn AI Data Engineering through hands-on development
- Build production-quality Python applications
- Implement Retrieval-Augmented Generation (RAG)
- Work with embeddings and vector databases
- Build REST APIs using FastAPI
- Containerize applications with Docker
- Deploy applications to the cloud
- Follow software engineering best practices

---

## 🛠 Tech Stack

### Current

- Python 3.x
- Git
- GitHub

### Planned

- FastAPI
- Docker
- OpenAI API / Gemini API
- FAISS
- LangChain
- LangGraph
- Vector Database
- Pytest
- Logging
- GitHub Actions

---

## 📂 Project Structure

```text
enterprise-knowledge-assistant/
│
├── data/
│   └── sample.txt
│
├── src/
│   └── main.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Current Features

- Read text documents
- Count total characters
- Count total lines
- Display document summary
- Handle common file-related exceptions

---

## 📌 Sample Output

```text
File loaded successfully

Total Characters : 125
Total Lines      : 5
File Path        : data/sample.txt
```

---

# 🗺 Roadmap

## Phase 1 — Python Foundations

- [x] Project setup
- [x] File handling
- [x] Exception handling
- [x] Character count
- [x] Line count
- [ ] Pathlib
- [ ] Logging
- [ ] Unit testing

---

## Phase 2 — Document Processing

- [ ] Read multiple documents
- [ ] Document parsing
- [ ] Text cleaning
- [ ] Chunking
- [ ] Metadata extraction

---

## Phase 3 — Search Engine

- [ ] Keyword search
- [ ] Ranking
- [ ] Similarity search

---

## Phase 4 — AI Integration

- [ ] Embeddings
- [ ] Vector database
- [ ] Semantic search
- [ ] Retrieval-Augmented Generation (RAG)
- [ ] LLM Integration

---

## Phase 5 — Production

- [ ] FastAPI
- [ ] Docker
- [ ] Configuration management
- [ ] Logging
- [ ] Unit testing
- [ ] CI/CD
- [ ] Cloud deployment

---

# 📅 Progress Log

## Day 1 (1 July 2026)

### Completed

- Project initialization
- Repository setup
- Text file reader
- Exception handling
- Document summary
- Character counting
- Line counting

### Concepts Learned

- File handling
- `with` statement
- `try-except`
- `pathlib` (Introduction)
- Functions
- Type hints
- Docstrings

# 📅 Progress Log

---

## ✅ Day 2 — Keyword-Based Document Search

### Objective

Build a simple search engine capable of retrieving relevant paragraphs from a text document without using AI.

### Features Implemented

- Split document into paragraphs
- Stored paragraphs in a Python list
- Accepted user input using `input()`
- Implemented keyword-based search
- Returned matching paragraphs
- Displayed user-friendly messages when no match was found

### Python Concepts Learned

- Functions
- Lists
- Loops
- String methods
- User Input
- List Comprehension
- Boolean Flags (`found = False`)

### Software Engineering Concepts

- Separation of Concerns
- Function Design
- Code Readability
- Incremental Development

### Challenges

- Designing search logic
- Working with lists of paragraphs
- Handling missing search results

### Commit

```text
feat: implement keyword-based document search
```

---

## ✅ Day 3 — Query Preprocessing

### Objective

Improve the search engine by cleaning user queries before performing the search.

### Features Implemented

- Built `clean_query()` utility function
- Converted queries to lowercase
- Removed punctuation (`?`)
- Removed stop words
- Improved search accuracy
- Created reusable text utility module

### Python Concepts Learned

- `strip()`
- `lower()`
- `replace()`
- `split()`
- `join()`
- String Iteration
- Type Hints
- Return Statements

### Software Engineering Concepts

- Query Normalization
- Stop Words
- Edge Case Analysis
- Utility Modules
- Function Reusability
- Debugging

### Challenges

- Understanding `return` inside vs outside loops
- Debugging indentation issues
- Testing multiple query formats
- Improving algorithm design

### Commit

```text
feat: add query preprocessing and text utility functions
```

---

### Current Project Status

- [x] Project Setup
- [x] File Reader
- [x] Exception Handling
- [x] Document Summary
- [x] Paragraph Splitting
- [x] Keyword Search
- [x] Query Preprocessing
- [ ] Keyword Indexing
- [ ] Ranking
- [ ] Semantic Search
- [ ] Embeddings
- [ ] Vector Database
- [ ] RAG Pipeline
- [ ] FastAPI
- [ ] Docker
- [ ] Deployment
---

# 🏗 Engineering Principles

This project follows:

- Clean Code
- Separation of Concerns
- Single Responsibility Principle (SRP)
- Modular Design
- Readable Code
- Production-first mindset
- Incremental development

---

# 📚 Learning Philosophy

This repository is intentionally built one feature at a time.

The objective is **not** to copy tutorial code, but to understand how production-grade AI applications are designed, developed, tested, and deployed.

Every feature is implemented only after understanding:

- Why it is required
- How it works
- Where it fits in the overall architecture
- Production best practices

---

# 👨‍💻 Author

**Geetesh Singh**

Data Engineer transitioning into AI Data Engineering through production-grade projects and continuous learning.

---

# ⭐ Future Scope

By the end of this project, the application will support:

- PDF ingestion
- OCR
- Multiple document formats
- Intelligent chunking
- Embedding generation
- Vector similarity search
- AI-powered question answering
- REST APIs
- Docker deployment
- Cloud deployment
- Enterprise-ready architecture

---

## 📄 License

This project is intended for educational purposes, portfolio development, and demonstration of AI Data Engineering concepts.

