import os
import fitz  # PyMuPDF
import chromadb
from dotenv import load_dotenv

load_dotenv()

# Initialize ChromaDB client (persistent storage)
CHROMA_DIR = "./chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_or_create_collection(name="financial_docs")

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from all pages of a PDF using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list:
    """Splits text into overlapping chunks manually."""
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    return chunks

def process_and_store_pdf(file_path: str):
    """Processes PDF, chunks it, and saves embeddings/text to ChromaDB."""
    raw_text = extract_text_from_pdf(file_path)
    chunks = chunk_text(raw_text)
    
    if not chunks:
        raise ValueError("No text found in the PDF.")
    
    # Clear old entries if any, or add new
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    
    # Add to ChromaDB (Chroma handles default embeddings if none provided, or we can store raw docs)
    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=[{"source": os.path.basename(file_path)} for _ in chunks]
    )
    
    return len(chunks)