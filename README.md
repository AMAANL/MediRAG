#  MediRAG — Clinical Decision Support AI

> **AI-powered Retrieval-Augmented Generation for rare disease diagnosis**
> Built with Google Gemini · PubMed · openFDA · ChromaDB · FastAPI · React

<img width="1461" height="747" alt="MediRAG Screenshot" src="https://github.com/user-attachments/assets/f4acf078-aa25-4c93-8b3a-b862db4c8684" />

---

##  What is MediRAG?

MediRAG is a full-stack, AI-powered **Clinical Decision Support Assistant** built for physicians facing rare or complex diagnoses. Instead of relying on an LLM's generalized training data (which can hallucinate), MediRAG uses a **RAG (Retrieval-Augmented Generation)** architecture to:

1.  **Pull real, trusted medical knowledge** from PubMed research articles and openFDA drug labels
2.  **Semantically search** that knowledge base for the most relevant passages to a physician's query
3.  **Ground the LLM's response exclusively in retrieved context**, ensuring every claim is backed by a real source
4.  **Return inline citations** so the physician can verify the original literature

The result is a medically grounded, hallucination-resistant AI assistant that thinks like a specialist librarian — retrieving evidence first, then forming conclusions.

---

##  End-to-End RAG Pipeline

```
 DATA SOURCES          INGESTION PIPELINE              QUERY PIPELINE
┌─────────────┐       ┌────────────────────┐          ┌──────────────────┐
│  PubMed API │──────▶│  Text Extraction   │          │ Physician Query  │
│ (50 papers) │       │  & Cleaning        │          │ + Patient Context│
└─────────────┘       └────────────────────┘          └────────┬─────────┘
                               │                               │
┌─────────────┐       ┌────────▼────────────┐          ┌───────▼─────────┐
│ openFDA API │──────▶│ Text Chunking       │          │ Query Embedding │
│ (30 labels) │       │ (500 chars, 50 ovlp)│          │ all-MiniLM-L6v2 │
└─────────────┘       └─────────────────────┘          └────────┬────────┘
                               │                                │
                      ┌────────▼────────────┐          ┌────────▼────────┐
                      │ Embedding Generation│◀──────── │                 │
                      │ all-MiniLM-L6-v2    │          │   ChromaDB      │
                      │ (384-dim vectors)   │─────────▶│ Semantic Search │
                      └─────────────────────┘          │   (Top-10)      │
                               │                       └────────┬────────┘
                      ┌────────▼────────────┐                   │
                      │     ChromaDB        │          ┌────────▼─────────┐
                      │  (365 indexed chunks│          │  Cross-Encoder   │
                      │   stored on disk)   │          │  Reranker (Top-5)│
                      └─────────────────────┘          └────────┬─────────┘
                                                                │
                                                      ┌─────────▼────────┐
                                                      │  Prompt Builder  │
                                                      │  System + Context│
                                                      │  + Query         │
                                                      └────────┬─────────┘
                                                               │
                                                      ┌────────▼─────────┐
                                                      │  Google Gemini   │
                                                      │  gemini-2.0-flash│
                                                      └────────┬─────────┘
                                                               │
                                                      ┌────────▼─────────┐
                                                      │ Grounded Response│
                                                      │ + Citations      │
                                                      └──────────────────┘
```

---
<img width="1536" height="1024" alt="End-to-end medical retrieval system infographic" src="https://github.com/user-attachments/assets/8bf87196-435a-4af1-b16b-35bc4a9e5a78" />
## 🔬 Pipeline Components Explained

### Phase 1 — Data Ingestion *(runs once offline)*

| Step | File | Description |
|------|------|-------------|
| **1. Fetch PubMed** | `data/ingestion/fetch_pubmed.py` | Queries the free PubMed Entrez API for 50 medical research abstracts on rare diseases |
| **2. Fetch FDA** | `data/ingestion/fetch_fda.py` | Pulls 30 drug labels from openFDA including indications, warnings, and interactions |
| **3. Chunk** | `pipeline/chunker.py` | Splits all text into 500-character chunks with 50-character overlap using LangChain's `RecursiveCharacterTextSplitter`. Produces **365 total chunks** |
| **4. Embed** | `pipeline/embedder.py` | Converts each chunk to a 384-dimensional vector using `sentence-transformers/all-MiniLM-L6-v2` — runs fully locally, no API key needed |
| **5. Index** | `pipeline/vector_store.py` | Persists all vectors + metadata (source, title, URL) into **ChromaDB** on disk |

### Phase 2 — Query Processing *(real-time, per request)*

| Step | File | Description |
|------|------|-------------|
| **6. Embed Query** | `pipeline/retriever.py` | Embeds the physician's query into the same 384-dim vector space |
| **7. Retrieve** | `pipeline/retriever.py` | ChromaDB cosine similarity search returns **Top-10** most relevant chunks |
| **8. Rerank** | `pipeline/reranker.py` | `cross-encoder/ms-marco-MiniLM-L-6-v2` scores all 10 passages vs. the query for precision. Selects **Top-5** |
| **9. Build Prompt** | `pipeline/prompt_builder.py` | Constructs a structured prompt: system role (expert clinical AI) + 5 context passages + physician query |
| **10. Generate** | `api/routes/query.py` | Google Gemini (`gemini-2.0-flash`) produces a grounded response using **only the retrieved context** |
| **11. Return Citations** | `api/routes/query.py` | Source metadata returned alongside the text so the physician can verify original papers |

---

##  Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 19 + Vite 8 + Tailwind CSS v4 | Clinical UI — symptom input, response display, citation cards |
| **Backend API** | FastAPI + Uvicorn | REST endpoints, CORS, serves production React build |
| **LLM** | Google Gemini `gemini-2.0-flash` | Grounded answer generation |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` | Vectorisation of documents and queries (local, free) |
| **Reranker** | `cross-encoder/ms-marco-MiniLM-L-6-v2` | Precision passage scoring (local, free) |
| **Vector DB** | ChromaDB (local persistent) | Fast semantic similarity search |
| **Chunker** | LangChain Text Splitters | Recursive character splitting |
| **Data Sources** | PubMed Entrez API + openFDA API | Free, authoritative medical knowledge corpus |
| **Deployment** | Hugging Face Spaces (Docker) | One-click public HTTPS hosting |

---

##  Project Structure

```
medirag/
├── api/
│   ├── main.py              # FastAPI app — CORS, routing, serves React build
│   └── routes/
│       └── query.py         # POST /query — orchestrates the full RAG pipeline
├── pipeline/
│   ├── chunker.py           # Text splitting logic
│   ├── embedder.py          # Embedding generation + ChromaDB indexing
│   ├── retriever.py         # Semantic search (Top-10 retrieval)
│   ├── reranker.py          # Cross-encoder reranking (Top-5)
│   ├── prompt_builder.py    # Constructs Gemini prompt with context
│   └── vector_store.py      # ChromaDB client wrapper
├── data/
│   └── ingestion/
│       ├── fetch_pubmed.py  # PubMed Entrez API fetcher (50 abstracts)
│       └── fetch_fda.py     # openFDA API fetcher (30 drug labels)
├── frontend/
│   └── src/
│       ├── App.jsx                      # Main layout + API integration
│       └── components/
│           ├── QueryInput.jsx           # Symptom & patient context form
│           ├── ResponseDisplay.jsx      # AI response renderer
│           └── CitationCard.jsx         # Source citation card
├── Dockerfile               # HF Spaces Docker deployment config
├── .env.example             # Environment variable template
└── requirements.txt         # Python dependencies
```

---

##  Local Setup & Running

### Prerequisites
- Python 3.10+
- Node.js 18+
- A free [Google Gemini API Key](https://aistudio.google.com/app/apikey)

### 1. Backend Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 2. Ingest & Build the Vector Database *(one-time)*

```bash
python data/ingestion/fetch_pubmed.py   # Fetch 50 PubMed abstracts
python data/ingestion/fetch_fda.py      # Fetch 30 FDA drug labels
python pipeline/embedder.py             # Embed & index into ChromaDB
```

### 3. Start the Backend

```bash
uvicorn api.main:app --reload --port 8000
```

### 4. Frontend Setup

```bash
cd frontend
npm install
npm run dev    # Runs on http://localhost:5173
```

The API will be available at `http://localhost:8000` and the React UI at `http://localhost:5173`.

---

## Live Demo

 **Hugging Face Space:** https://huggingface.co/spaces/Amaanlakdawala/MediRAG-Clinical-Assistant

---

##  Disclaimer

MediRAG is a research prototype built for the RAGx Hackathon. It is **not a substitute for professional medical advice, diagnosis, or treatment.** Always consult a qualified physician.
