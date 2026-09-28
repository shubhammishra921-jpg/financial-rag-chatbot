# 📊 Financial RAG Chatbot (Zero-LangChain Architecture)

A production-ready, ultra-lightweight Retrieval-Augmented Generation (RAG) system built to query and analyze complex financial PDF reports. Designed with a modular, dependency-hell-free architecture using **FastAPI**, **ChromaDB**, **PyMuPDF**, and direct **Google Gemini AI SDK**.

---

## 🚀 Key Features

* **Zero-LangChain Architecture:** Built with pure Python to completely eliminate version conflicts, heavy wrapper overhead, and runtime breaking changes.
* **Efficient PDF Processing:** Utilizes PyMuPDF (`fitz`) for fast text extraction and custom overlapping chunking algorithms.
* **Vector Search with ChromaDB:** Persistent local vector database for fast, accurate context retrieval.
* **Direct Gemini Integration:** Directly leverages Google Gemini models for hallucination-free, strict context-bound financial answering.
* **FastAPI Backend:** Fully documented REST API endpoints (`/upload-pdf/`, `/ask/`) with Swagger UI support.
* **Streamlit Frontend:** Clean, user-friendly interactive web UI for seamless document uploading and conversational querying.

---

## 🛠️ Tech Stack

* **Backend & API:** Python, FastAPI, Uvicorn, Pydantic
* **AI / LLM:** Google Gemini API (`gemini-pro`)
* **Vector Database:** ChromaDB
* **PDF Parsing:** PyMuPDF (`fitz`)
* **Frontend:** Streamlit, Requests

---

## 📁 Project Structure

```text
financial-rag-chatbot/
│
├── app.py                # FastAPI main application & routes
├── rag_engine.py         # PDF extraction, chunking, and ChromaDB integration
├── qa_engine.py          # Gemini AI retrieval & context generation logic
├── streamlit_app.py      # Streamlit interactive frontend dashboard
├── requirements.txt      # Lightweight project dependencies
├── .env                  # Environment variables (API keys)
└── README.md             # Project documentation