
# RAG API

This project provides a simple Retrieval-Augmented Generation (RAG) API using FastAPI, ChromaDB, and Ollama. It enables dynamic knowledge base management and natural language querying over embedded documents.

## Features
- REST API endpoints to query and add knowledge
- Uses ChromaDB for persistent vector storage and retrieval
- Integrates with Ollama for LLM-based question answering
- Embedding utility to store documents (e.g., Kubernetes notes) in the database
- Health check endpoint for service monitoring

## Setup
1. **Clone the repository:**
	```sh
	git clone https://github.com/ashi-ish/RAG-API.git
	cd RAG-API
	```
2. **Create a virtual environment and activate it:**
	```sh
	python3 -m venv venv
	source venv/bin/activate
	```
3. **Install dependencies:**
	```sh
	pip install fastapi uvicorn chromadb ollama
	```
4. **Install and start Ollama:**
	- Download from https://ollama.com/download
	- Start the server:
	  ```sh
	  ollama serve
	  ```
5. **Run the FastAPI server:**
	```sh
	uvicorn app:app --reload
	```

## API Endpoints

### Add Knowledge
Add new content to the knowledge base.
```
POST /add
Body (form or JSON): { "text": "<your content>" }
```

### Query
Query the knowledge base with natural language.
```
POST /query
Body (form or JSON): { "q": "<your question>" }
```

### Health Check
```
GET /health
```

## Embedding Documents
To embed a document (e.g., Kubernetes notes):
1. Place your text in `k8s.txt`.
2. Run:
	```sh
	python embed.py
	```
This will store the embedding in the Chroma database.

## Example
**Query Example:**
```sh
curl -X POST "http://127.0.0.1:8000/query" -G --data-urlencode "q=What is Kubernetes?"
```

## Tech Stack
- Python
- FastAPI
- ChromaDB
- Ollama

## Folder Structure
- `app.py`: Main API server
- `embed.py`: Script to embed documents
- `db/`: Persistent ChromaDB storage
 - `k8s.txt`: Example document for embedding

## Docker
You can run the API using Docker:

1. **Build the Docker image:**
	```sh
	docker build -t rag-api .
	```
2. **Run the container:**
	```sh
	docker run -p 8000:8000 rag-api
	```

> **Note:**
> - The Dockerfile installs all dependencies and runs the embedding script at build time.
> - You still need to have the Ollama server running and accessible from the container host.
> - If you want to connect to a remote Ollama server, set the appropriate environment variables or network configuration.
