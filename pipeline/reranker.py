from sentence_transformers import CrossEncoder

model_name = "cross-encoder/ms-marco-MiniLM-L-6-v2"
reranker = CrossEncoder(model_name)

def rerank_chunks(query: str, chunks: list, top_k: int = 5):
    """
    Reranks chunks using a cross-encoder model.
    """
    if not chunks:
        return []
        
    pairs = [[query, chunk["text"]] for chunk in chunks]
    scores = reranker.predict(pairs)
    
    # Add scores to chunks and sort
    for i, chunk in enumerate(chunks):
        chunk["rerank_score"] = float(scores[i])
        
    ranked_chunks = sorted(chunks, key=lambda x: x["rerank_score"], reverse=True)
    return ranked_chunks[:top_k]
