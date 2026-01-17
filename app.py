from fastapi import FastAPI
import chromadb
from ollama import Client
import os
import logging
import uuid

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


MODEL_NAME = os.getenv("MODEL_NAME", "tinyllama")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
logging.info(f"Using model: {MODEL_NAME}")
logging.info(f"Ollama endpoint: {OLLAMA_BASE_URL}")

ollama_client = Client(host=OLLAMA_BASE_URL)

app = FastAPI()
chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection("docs")

@app.post("/query")
def query(q: str):
    try:
        results = collection.query(query_texts=[q], n_results=1)
        context = results["documents"][0][0] if results["documents"] else ""

        answer = ollama_client.generate(
            model=MODEL_NAME,
            prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:"
        )
        return {"answer": answer["response"]}
    except Exception as e:
        logging.exception("Error in /query endpoint")
        return {"error": str(e)}

@app.post("/add")
def add_knowledge(text: str):
    """Add new content to the knowledge base dynamically."""
    try:
        # Generate a unique ID for this document
        doc_id = str(uuid.uuid4())
        
        # Add the text to Chroma collection
        collection.add(documents=[text], ids=[doc_id])
        
        return {
            "status": "success",
            "message": "Content added to knowledge base",
            "id": doc_id
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/health")
def health():
    return {"status": "ok"}
