---
title: MediRAG Clinical Assistant
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# MediRAG: Clinical Decision Support Assistant

MediRAG is a full-stack AI-powered Retrieval-Augmented Generation (RAG) application that helps physicians diagnose rare diseases by fetching data from trusted medical sources (PubMed and openFDA) and generating cited, grounded responses.

## Setup Instructions

### 1. Backend Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy the environment variables:
   ```bash
   cp .env.example .env
   ```
   **Important**: Add your `OPENAI_API_KEY` to the `.env` file.

3. Complete the Initial Ingestion and Indexing Pipeline:
   Run these scripts in order to set up your vector database before launching the backend:
   ```bash
   python data/ingestion/fetch_pubmed.py
   python data/ingestion/fetch_fda.py
   python pipeline/embedder.py
   ```

4. Start the backend Server:
   ```bash
   uvicorn api.main:app --reload --port 8000
   ```

### 2. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install NPM dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

## Architecture

- **Backend Context:** `FastAPI` + `ChromaDB` localized vector store (no external API keys for DB required).
- **Retrieval Pipeline:** Embed queries using `sentence-transformers`, fetch top-10 chunks from vector store, and rerank with `cross-encoder`.
- **Generation:** Generates insights using `gpt-4o-mini` while exclusively using injected context snippets.
- **Frontend Context:** `React`, `TailwindCSS` with dark navy, white, and teal medical aesthetic. Responsive layout tracking symptoms and giving citations.
