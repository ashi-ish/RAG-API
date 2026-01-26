
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
Add new content to the knowledge base dynamically.
```
POST /add?text=<your content>
```
**Example:**
```sh
curl -X POST "http://127.0.0.1:8000/add" -G --data-urlencode "text=Kubernetes is a container orchestration platform."
```

### Query
Query the knowledge base with natural language.
```
POST /query?q=<your question>
```
**Example:**
```sh
curl -X POST "http://127.0.0.1:8000/query" -G --data-urlencode "q=What is Kubernetes?"
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



## Environment Variables

The application supports the following environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_NAME` | `tinyllama` | Ollama model to use for generation |
| `OLLAMA_BASE_URL` | `http://127.0.0.1:11434` | Ollama server endpoint |

**Example:**
```sh
export MODEL_NAME=llama2
export OLLAMA_BASE_URL=http://localhost:11434
uvicorn app:app --reload
```

## Tech Stack
- Python 3.11
- FastAPI
- ChromaDB (persistent vector storage)
- Ollama (LLM inference)
- Kubernetes (deployment)
- Docker (containerization)

## Folder Structure
```
rag-api/
├── app.py              # Main FastAPI server with /query, /add, /health endpoints
├── embed.py            # Script to embed documents into ChromaDB
├── k8s.txt             # Example document for embedding
├── Dockerfile          # Container image definition
├── deployment.yaml     # Kubernetes deployment manifest
├── service.yaml        # Kubernetes service manifest (NodePort type)
├── db/                 # Persistent ChromaDB storage directory
│   ├── chroma.sqlite3  # ChromaDB SQLite database
│   └── e9b3cd12.../    # Vector embeddings storage
└── README.md           # This file
```

## Docker

### Build and Run Locally

1. **Build the Docker image:**
	```sh
	docker build -t rag-app .
	```

2. **Run the container:**
	```sh
	docker run -p 8000:8000 \
	  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
	  -e MODEL_NAME=tinyllama \
	  rag-app
	```

> **Notes:**
> - The Dockerfile uses Python 3.11-slim base image
> - Automatically runs `embed.py` during build to populate the knowledge base with `k8s.txt`
> - On macOS/Windows Docker Desktop, use `host.docker.internal` to access host services
> - On Linux, use `--network=host` or the host's IP address

## Kubernetes Deployment (Minikube)

Deploy the RAG API to a local Kubernetes cluster using Minikube:

### Prerequisites
- Minikube installed and running
- kubectl configured to use Minikube context
- Docker (for building images)
- Ollama installed and running on your host machine:
  ```sh
  # Install from https://ollama.com/download
  ollama serve
  ollama pull tinyllama
  ```

### Deployment Steps

1. **Start Minikube (if not already running):**
	```sh
	minikube start
	```

2. **Build the Docker image in Minikube's environment:**
	```sh
	eval $(minikube docker-env)
	docker build -t rag-app .
	```

3. **Apply Kubernetes manifests:**
	```sh
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml
	```
	
	This creates:
	- A Deployment with 1 replica running the rag-app container
	- A NodePort Service exposing port 8000

4. **Port forward to access the API:**
	```sh
	kubectl port-forward service/rag-app-service 8000:8000
	```
	Or get the Minikube service URL:
	```sh
	minikube service rag-app-service --url
	```

### Configuration

The deployment is configured to connect to Ollama running on your host machine:
- **Environment Variable:** `OLLAMA_BASE_URL=http://host.minikube.internal:11434`
- This allows the containerized app to access Ollama on your host system
- The model used is `tinyllama` (configurable via `MODEL_NAME` env var)

### Verify Deployment
```sh
# Check pod status
kubectl get pods

# Check logs
kubectl logs -f deployment/rag-app-deployment

# Test the API
curl -X POST "http://127.0.0.1:8000/query" -G --data-urlencode "q=What is Kubernetes?"
```

### Troubleshooting

**Failed to connect to Ollama:**
- Verify Ollama is running: `curl http://localhost:11434/api/version`
- Check the model is available: `ollama list`
- Pull the model if needed: `ollama pull tinyllama`
- Verify Minikube host access: `minikube ssh "grep host.minikube.internal /etc/hosts"`

**Pod not starting:**
- Check logs: `kubectl logs -f deployment/rag-app-deployment`
- Verify image is built: `eval $(minikube docker-env) && docker images | grep rag-app`
- Check pod events: `kubectl describe pod <pod-name>`

**Port forwarding issues:**
- Ensure no other service is using port 8000
- Use `minikube service rag-app-service --url` as an alternative
- Check service status: `kubectl get svc rag-app-service`
