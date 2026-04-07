from sentence_transformers import SentenceTransformer
from pipeline.vector_store import query_vector_store
import os

# Load model globally to avoid reloading on each request
# We'll use the fallback lighter model for speed
model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
embedder = SentenceTransformer(model_name)

def retrieve_chunks(query: str, top_n: int = 10):
    """
    Embeds the user query and retrieves top-10 chunks from ChromaDB.
    """
    query_embedding = embedder.encode(query).tolist()
    results = query_vector_store(query_embedding, n_results=top_n)
    
    retrieved_chunks = []
    if results['documents'] and len(results['documents'][0]) > 0:
        docs = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results['distances'][0] if 'distances' in results else []
        ids = results['ids'][0]
        
        for i in range(len(docs)):
            retrieved_chunks.append({
                "id": ids[i],
                "text": docs[i],
                "metadata": metadatas[i],
                "distance": distances[i] if i < len(distances) else None
            })
            
    return retrieved_chunks
