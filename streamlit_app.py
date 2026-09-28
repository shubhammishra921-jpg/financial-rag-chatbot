import streamlit as st
import requests

st.set_page_config(page_title="Financial RAG Chatbot", layout="centered")

st.title("📊 Financial RAG Chatbot")
st.write("Upload your financial PDF report and ask questions directly from it.")

# FastAPI backend URL
API_URL = "https://financial-rag-backend-dnnf.onrender.com"

# Sidebar for PDF Upload
st.sidebar.header("Upload Financial PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    if st.sidebar.button("Process PDF"):
        with st.spinner("Processing PDF and storing in ChromaDB..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            try:
                response = requests.post(f"{API_URL}/upload-pdf/", files=files)
                if response.status_code == 200:
                    st.sidebar.success("PDF processed successfully!")
                else:
                    st.sidebar.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.sidebar.error(f"Could not connect to FastAPI server: {e}")

# Main Chat Interface
st.header("💬 Ask Questions")
question = st.text_input("Enter your question about the financial document:")

if st.button("Get Answer"):
    if question:
        with st.spinner("Analyzing document with Gemini..."):
            try:
                response = requests.post(f"{API_URL}/ask/", params={"question": question})
                if response.status_code == 200:
                    data = response.json()
                    st.success("Answer:")
                    st.write(data.get("answer"))
                    
                    sources = data.get("sources", [])
                    if sources:
                        st.info(f"Sources: {', '.join(sources)}")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Could not connect to FastAPI server: {e}")
    else:
        st.warning("Please enter a question.")