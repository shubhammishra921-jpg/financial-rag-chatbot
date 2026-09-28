from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os
from rag_engine import process_and_store_pdf
from qa_engine import query_financial_rag

app = FastAPI(title="Financial RAG Chatbot API (Pure Python)", version="2.0")

UPLOAD_DIR = "./uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "Welcome to the Clean Financial RAG Chatbot API!"}

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """Uploads a financial PDF and processes it into ChromaDB."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        chunks_count = process_and_store_pdf(file_path)
        return {"filename": file.filename, "chunks_created": chunks_count, "message": "PDF processed and stored successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask/")
async def ask_question(question: str):
    """Answers a question based on the uploaded financial PDF."""
    try:
        result = query_financial_rag(question)
        return {
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))