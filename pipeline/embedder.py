import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sentence_transformers import SentenceTransformer
from pipeline.chunker import load_and_chunk_data
from pipeline.vector_store import add_documents

def generate_embeddings_and_index():
    """
    Loads chunks, generates embeddings using sentence-transformers,
    and adds them to the ChromaDB vector store.
    """
    model_name = "all-MiniLM-L6-v2"  # Lighter/faster fallback
    print(f"Loading embedding model: {model_name}...")
    model = SentenceTransformer(model_name)
    
    print("Loading and chunking data...")
    chunks_data = load_and_chunk_data()
    
    if not chunks_data:
        print("No chunks to process. Please run ingestion scripts first.")
        return
        
    texts = [item["text"] for item in chunks_data]
    metadatas = [item["metadata"] for item in chunks_data]
    
    print(f"Generating embeddings for {len(texts)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True)
    
    print("Adding documents to vector store...")
    add_documents(texts, embeddings.tolist(), metadatas)
    print("Indexing complete.")

if __name__ == "__main__":
    generate_embeddings_and_index()
