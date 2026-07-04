# Enterprise Knowledge Assistant

> 🚀 A production-oriented AI Data Engineering project that evolves from basic document processing into a Retrieval-Augmented Generation (RAG) application using modern AI technologies.

---

## 📌 Project Status

**Current Phase:** Phase 1 – Python Foundations

**Progress:** Day 3 / 90

### Current Capabilities

- ✅ Read text documents
- ✅ Display document summary
- ✅ Split documents into paragraphs
- ✅ Perform keyword-based search
- ✅ Query preprocessing
- ✅ Stop-word removal
- ✅ Exception handling

---

## 📖 Overview

Enterprise organizations store vast amounts of information across documents such as PDFs, Word files, SOPs, emails, reports, and knowledge bases.

This project demonstrates how to build an AI-powered Enterprise Knowledge Assistant capable of ingesting enterprise documents, retrieving relevant information, and eventually answering user questions using Retrieval-Augmented Generation (RAG).

Unlike tutorial-based projects, this repository is being developed incrementally using production engineering practices.

---

# 🏛 Current Architecture

```text
                User
                  │
                  ▼
          Enter Search Query
                  │
                  ▼
        Query Preprocessing
                  │
                  ▼
      Keyword-Based Search
                  │
                  ▼
      Matching Paragraph(s)
                  │
                  ▼
             Response
```

---

# 🎯 Goals

- Learn AI Data Engineering by building real projects
- Master Python from fundamentals to advanced
- Build production-quality software
- Learn Retrieval-Augmented Generation (RAG)
- Work with Embeddings
- Integrate Vector Databases
- Build REST APIs using FastAPI
- Containerize applications using Docker
- Deploy applications to the cloud

---

# 🛠 Tech Stack

## Current

- Python 3.x
- Git
- GitHub

## Planned

- FastAPI
- Docker
- OpenAI API
- Gemini API
- FAISS
- LangChain
- LangGraph
- Vector Database
- Pytest
- Logging
- GitHub Actions

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

- Read text files
- Character counting
- Line counting
- Document summary
- Paragraph splitting
- Keyword search
- Query preprocessing
- Stop-word removal

## Planned

- Keyword indexing
- Ranking engine
- Semantic search
- Embeddings
- Vector database
- RAG
- FastAPI
- Docker
- Cloud deployment

---

# 🗺 Roadmap

## Phase 1 — Python Foundations

- [x] Project setup
- [x] File handling
- [x] Exception handling
- [x] Character count
- [x] Line count
- [x] Functions
- [x] Pathlib
- [ ] Logging
- [ ] Unit testing

---

## Phase 2 — Document Processing

- [x] Paragraph splitting
- [x] Query preprocessing
- [ ] Read multiple documents
- [ ] Text cleaning
- [ ] Chunking
- [ ] Metadata extraction

---

## Phase 3 — Search Engine

- [x] Keyword search
- [ ] Keyword indexing
- [ ] Ranking
- [ ] Similarity search

---

## Phase 4 — AI Integration

- [ ] Embeddings
- [ ] Vector Database
- [ ] Semantic Search
- [ ] RAG
- [ ] LLM Integration

---

## Phase 5 — Production

- [ ] FastAPI
- [ ] Docker
- [ ] Configuration
- [ ] Logging
- [ ] Unit Testing
- [ ] CI/CD
- [ ] Cloud Deployment

---

# 📅 Development Journal

## ✅ Day 1 — File Reader

### Features

- Project initialization
- File reader
- Exception handling
- Character count
- Line count

### Python Concepts

- File Handling
- Functions
- Type Hints
- Docstrings
- try-except
- pathlib

---

## ✅ Day 2 — Keyword Search

### Features

- Paragraph splitting
- Keyword search
- User input
- Search results

### Python Concepts

- Lists
- Loops
- List Comprehension
- Boolean Flags

---

## ✅ Day 3 — Query Preprocessing

### Features

- clean_query()
- Stop-word removal
- Query normalization
- Utility module

### Python Concepts

- split()
- join()
- lower()
- strip()
- replace()
- String iteration

### Biggest Lesson

> The position of a `return` statement completely changes program flow.

---

# 🏗 Engineering Principles

- Clean Code
- Single Responsibility Principle (SRP)
- Separation of Concerns
- Modular Design
- Incremental Development
- Production-first Mindset

---

# 📚 Learning Philosophy

This project is intentionally built from scratch without relying on large tutorials.

Every feature is implemented only after understanding:

- Why it is needed
- How it works
- Trade-offs
- Production best practices

---

# 📈 Current Progress

```text
████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 3%
```

Current Milestone

✅ Python Foundations

⬜ Smarter Search

⬜ Semantic Search

⬜ Embeddings

⬜ Vector Database

⬜ RAG

⬜ FastAPI

⬜ Docker

⬜ Deployment

---

# 👨‍💻 Author

**Geetesh Singh**

Data Engineer transitioning into AI Data Engineering by building production-grade projects from scratch.

---

# 📄 License

This repository is intended for learning, portfolio development, and demonstration purposes.