import chromadb
import os

# Ensure chromadb path is correct relative to execution context
DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
COLLECTION_NAME = "medirag_knowledge"

def get_collection():
    """
    Initializes and returns the ChromaDB collection.
    """
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    return collection

def add_documents(texts, embeddings, metadatas):
    """
    Adds chunks and their embeddings to the ChromaDB collection.
    """
    collection = get_collection()
    
    # Generate deterministic IDs based on metadata
    ids = [f"{md['article_id']}_chunk_{md['chunk_index']}" for md in metadatas]
    
    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

def query_vector_store(embedding, n_results=10):
    """
    Queries ChromaDB for the most similar chunks.
    """
    collection = get_collection()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )
    return results
