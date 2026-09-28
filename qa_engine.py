import os
import chromadb
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

CHROMA_DIR = "./chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)

def query_financial_rag(question: str):
    """Retrieves relevant chunks from ChromaDB and generates an answer using Gemini."""
    try:
        collection = chroma_client.get_collection(name="financial_docs")
    except Exception:
        return {"answer": "No financial report found. Please upload a PDF first.", "sources": []}
    
    # Query ChromaDB for top 3 relevant chunks
    results = collection.query(
        query_texts=[question],
        n_results=3
    )
    
    retrieved_docs = results.get("documents", [[]])[0]
    sources = set([meta.get("source", "Unknown") for meta in results.get("metadatas", [[]])[0]])
    
    if not retrieved_docs:
        return {"answer": "I could not find any relevant information in the uploaded document.", "sources": []}
    
    # Construct context for Gemini
    context = "\n\n---\n\n".join(retrieved_docs)
    
    prompt = f"""
    You are a strict financial assistant AI. Answer the user's question using ONLY the context provided below. 
    If the answer cannot be found in the context, state clearly: "This information is not available in the provided financial report."
    Do not assume or make up facts.

    Context:
    {context}

    Question: {question}
    
    Answer:
    """
    
    # Call Gemini Flash model directly
    model = genai.GenerativeModel("gemini-3.8-flash")
    response = model.generate_content(prompt)
    
    return {
        "answer": response.text.strip(),
        "sources": list(sources)
    }