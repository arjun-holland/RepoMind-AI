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

### Render Deployment Configuration (Manual)
Since Render Blueprints require a paid plan, you can deploy the two services manually for free by connecting your GitHub repository.

#### 1. Backend Web Service
Create a **New Web Service** and carefully select the following options:
1. Connect your GitHub repository.
2. Select **Language**: `Docker`.
3. Under the advanced section, set **Dockerfile Path**: `Dockerfile.backend`.
4. Add your Environment Variables:
   - `MONGO_URI`: Your MongoDB connection string.
   - `GEMINI_API_KEY`: Your Gemini API key.

#### 2. Frontend Web Service
Create another **New Web Service** (or a free Static Site, but Docker is recommended for Nginx proxying):
1. Connect the exact same GitHub repository.
2. Select **Language**: `Docker`.
3. Under the advanced section, set **Dockerfile Path**: `Dockerfile.frontend`.

*Important: Render will give your Backend an auto-generated URL (e.g., `https://ai-codebase-api.onrender.com`). You may need to update the `nginx.conf` and explicitly replace `proxy_pass http://backend:8000/api/;` with your actual Render Backend URL!*

## Flow

1. **Upload Page (`/`):** Paste a public repository link. The backend will spawn a background thread, cloning, chunking and embedding the codebase in ChromaDB (using `all-MiniLM-L6-v2` locally).
2. **Chat Page (`/chat`):** Ask questions referencing the uploaded repository. Top-match contextual snippets (and AST function mapping) will feed a prompt responding with exact code references powered by Google's `gemini-2.5-flash` model.
