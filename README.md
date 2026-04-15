# 🧠 AI-Based Research Paper Assistant

An AI-powered research assistant that helps users **search, analyze, compare, and understand research papers efficiently** using Semantic Search, LLMs, and Retrieval-Augmented Generation (RAG).

---

## 🚀 Overview

The AI-Based Research Paper Assistant is designed to simplify academic workflows by combining:

- 🔍 Semantic Search (real-time papers from arXiv)
- 📄 AI Summarization
- 💬 Chat with Research Papers
- 📊 Paper Comparison
- 📚 Document-based Q&A

This system enables researchers and students to **quickly find relevant papers, understand them, and compare different approaches**.

---

## 🔥 Features

### 🔍 Semantic Search (NEW 🔥)
- Fetch real-time research papers from arXiv API
- Convert papers into embeddings (MiniLM)
- Perform cosine similarity search
- Return top relevant papers with similarity score

---

### 📄 AI Summarization
- Automatically generate concise summaries of research papers
- Uses Groq LLM (LLaMA 3.1)

---

### 💬 Chat with Paper (Deconstructor)
- Upload PDF research papers
- Ask questions interactively
- Context-aware responses using vector retrieval

---

### 📊 Paper Comparison (NEW 🔥)
- Upload multiple PDFs
- Generate summaries for each paper
- Compare based on:
  - Methodology
  - Results
  - Advantages & Disadvantages
  - Conclusion

---

### 🏗 Constructor (Paper Generator)
- Convert GitHub repositories into IEEE-style research papers
- Analyze codebase structure and documentation
- Generate structured academic content

---

## 🧠 Tech Stack

### Frontend
- Streamlit

### Backend / AI Layer
- Python

### LLM Provider
- Groq  
  - `llama-3.1-8b-instant`
  - `llama-3.1-70b-versatile`

### Embeddings
- Sentence Transformers  
  - `all-MiniLM-L6-v2`

### Vector Databases
- FAISS (Constructor)
- ChromaDB (Deconstructor)

### APIs
- arXiv API (real-time research papers)

### Database
- SQLite (sessions + chat history)

### PDF Handling
- PyMuPDF (fitz)
- ReportLab

---

## 🏗️ Architecture
```
User Query
↓
Fetch Papers (arXiv API)
↓
Embedding Model (MiniLM)
↓
Vector Similarity (Cosine / FAISS)
↓
Top Relevant Papers
↓
LLM (Groq) → Summary / Comparison / Chat

## 📁 Project Structure


research-paper-assistant/
│
├── home.py
├── pages/
│ ├── Constructor.py
│ ├── Deconstructor.py
│ ├── SemanticSearch.py 🔥 NEW
│ └── Comparison.py 🔥 NEW
│
├── constructor/
├── deconstructor/
├── shared/
├── data/
└── docs/


🧪 Usage
🔍 Semantic Search
Enter research topic
Get top relevant papers
View similarity scores
📊 Paper Comparison
Upload 2+ PDFs
Click compare
Get structured comparison
💬 Chat with Paper
Upload PDF
Ask questions
Get contextual answers
📄 Generate Paper
Enter GitHub repo link
Generate IEEE-style paper
🧠 Key Concepts Used
Semantic Search (Embeddings + Cosine Similarity)
Retrieval-Augmented Generation (RAG)
Large Language Models (LLMs)
Vector Databases (FAISS, ChromaDB)
NLP (Text Processing, Summarization)
🚀 Future Improvements
Hybrid Search (Keyword + Vector)
LLM-based re-ranking
Citation Graph Visualization
Semantic Scholar API integration
Multi-paper dashboard comparison
⚠️ Notes
Do NOT commit .env
First run downloads embedding model (~400MB)
arXiv results depend on query quality
📌 Project Highlights

✅ Real-time research paper retrieval
✅ Semantic similarity search
✅ AI-powered comparison system
✅ Full-stack AI application
✅ Production-level architecture

📜 License

Educational and research use only.
```
