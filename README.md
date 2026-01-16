# RAG API

This project provides a simple Retrieval-Augmented Generation (RAG) API using FastAPI, ChromaDB, and Ollama. It enables dynamic knowledge base management and natural language querying over embedded documents.

**Features:**
- REST API endpoints to query and add knowledge.
- Uses ChromaDB for persistent vector storage and retrieval.
- Integrates with Ollama for LLM-based question answering.
- Embedding utility to store documents (e.g., Kubernetes notes) in the database.
- Health check endpoint for service monitoring.

**Usage:**
- Add new content to the knowledge base via `/add`.
- Query the knowledge base with natural language via `/query`.
- Embeddings are managed and stored in the local ChromaDB instance.

**Tech Stack:** Python, FastAPI, ChromaDB, Ollama

**Folder Structure:**
- `app.py`: Main API server.
- `embed.py`: Script to embed documents.
- `db/`: Persistent ChromaDB storage.
- `k8s.txt`: Example document for embedding.
