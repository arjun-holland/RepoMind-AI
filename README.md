# AI Codebase Assistant

A production-ready codebase indexing system using Django REST Framework, Langchain, and ChromaDB. It ingests GitHub repositories, splits source code into chunks, extracts AST metadata from Python files, maps semantic meanings using local HuggingFace embeddings, and answers developer questions via a RAG interface over a sleek React frontend using the Gemini free tier API (`gemini-2.5-flash`).

## Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **MongoDB** (Local instance on `mongodb://localhost:27017` or cloud URI)
- **Gemini API Key** (Google AI Studio)

## Project Scaffolding
- `backend/`: Django and DRF REST API.
- `frontend/`: React + Vite + Tailwind CSS Application.

## Setup

### 1. Backend

1. **Virtual Environment & Dependencies**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Modify `.env` in the project root:
   ```env
   MONGO_URI=mongodb://localhost:27017/  # Or your MongoDB Atlas URI
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Database Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Run Server**
   ```bash
   python manage.py runserver
   ```

### 2. Frontend

1. **Navigate and Install**
   ```bash
   cd frontend
   npm install
   ```

2. **Run Dev Server**
   ```bash
   npm run dev
   ```

Navigate to `http://localhost:5173/` inside your browser to open the Codebase Assistant. 

## Docker Deployment (Production)

This project is configured for cloud deployment (e.g., Render) using Docker. 

### Local Docker Testing
You can quickly spin up both the frontend and backend using Docker Compose:
```bash
docker-compose up --build
```
- Frontend will be available at `http://localhost/`
- Backend API will be available at `http://localhost:8000/`

### Render Deployment Configuration
The project includes a `render.yaml` infrastructure-as-code file for one-click deployments. It provisions two services:
1. **Frontend**: Using `Dockerfile.frontend` (Node build + Nginx).
2. **Backend**: Using `Dockerfile.backend` (Django + Gunicorn).

**Environment Variables Required on Render:**
- `MONGO_URI`: Your MongoDB Atlas connection string.
- `GEMINI_API_KEY`: Your Google AI Studio API key.

## Flow

1. **Upload Page (`/`):** Paste a public repository link. The backend will spawn a background thread, cloning, chunking and embedding the codebase in ChromaDB (using `all-MiniLM-L6-v2` locally).
2. **Chat Page (`/chat`):** Ask questions referencing the uploaded repository. Top-match contextual snippets (and AST function mapping) will feed a prompt responding with exact code references powered by Google's `gemini-2.5-flash` model.
