from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import sys

# Ensure the root directory is in sys.path
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path)

# Try both absolute and relative imports for maximum compatibility
try:
    from api.routes import query
except ImportError:
    from routes import query

app = FastAPI(title="MediRAG API", description="Clinical decision support assistant")

# CORS setup for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"], # Added 5173 for Vite default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router)

# Serve the production React frontend if it exists
frontend_dist = os.path.join(root_path, "frontend", "dist")

if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Serve static files from root like vite.svg if they exist
        potential_file = os.path.join(frontend_dist, full_path)
        if full_path and os.path.isfile(potential_file):
            return FileResponse(potential_file)
            
        # Fallback to index.html for React Router
        return FileResponse(os.path.join(frontend_dist, "index.html"))
else:
    @app.get("/")
    def read_root():
        """Returns API info"""
        return {"message": "Welcome to MediRAG API", "version": "1.0", "status": "active"}
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/ingest")
async def trigger_ingestion(background_tasks: BackgroundTasks):
    """
    Triggers data fetching, embedding, and indexing programmatically.
    Runs as a background task.
    """
    def run_ingestion_pipeline():
        from data.ingestion.fetch_pubmed import fetch_pubmed_articles
        from data.ingestion.fetch_fda import fetch_fda_drugs
        from pipeline.embedder import generate_embeddings_and_index
        
        print("Starting ingestion pipeline...")
        fetch_pubmed_articles()
        fetch_fda_drugs()
        generate_embeddings_and_index()
        print("Ingestion pipeline completed.")

    background_tasks.add_task(run_ingestion_pipeline)
    return {"message": "Ingestion pipeline triggered in the background. Check backend console for progress."}
