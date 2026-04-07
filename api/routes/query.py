import os
import sys

# Ensure the root directory is in sys.path for absolute imports
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if root_path not in sys.path:
    sys.path.append(root_path)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

from pipeline.retriever import retrieve_chunks
from pipeline.reranker import rerank_chunks
from pipeline.prompt_builder import build_prompt

load_dotenv()
router = APIRouter()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class QueryRequest(BaseModel):
    symptoms: str
    patient_context: str = ""

class Source(BaseModel):
    title: str
    source: str
    url: str

class QueryResponse(BaseModel):
    diagnosis: str
    sources: list[Source]
    confidence: str

@router.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    """
    Handles POST /query: Embed -> Retrieve -> Rerank -> Prompt -> LLM
    """
    try:
        combined_query = f"{request.symptoms} {request.patient_context}".strip()
        
        # 1. Retrieve
        top_k_retrieve = int(os.getenv("TOP_K_RETRIEVE", 10))
        retrieved_chunks = retrieve_chunks(combined_query, top_n=top_k_retrieve)
        
        if not retrieved_chunks:
            return QueryResponse(
                diagnosis="No relevant medical context found in the knowledge base.",
                sources=[],
                confidence="Low"
            )
            
        # 2. Rerank
        top_k_rerank = int(os.getenv("TOP_K_RERANK", 5))
        ranked_chunks = rerank_chunks(combined_query, retrieved_chunks, top_k=top_k_rerank)
        
        # Extract unique sources for response
        unique_sources = {}
        for chunk in ranked_chunks:
            source_id = chunk['metadata'].get('article_id', 'unknown')
            if source_id not in unique_sources:
                unique_sources[source_id] = Source(
                    title=chunk['metadata'].get('title', 'Unknown Title'),
                    source=chunk['metadata'].get('source', 'Unknown Source'),
                    url=chunk['metadata'].get('url', '#')
                )
        
        # 3. Build Prompt
        system_instruction, user_content = build_prompt(request.symptoms, request.patient_context, ranked_chunks)
        
        # 4. LLM Generation
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_content,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
                max_output_tokens=1000
            )
        )
        
        diagnosis_text = response.text
        
        return QueryResponse(
            diagnosis=diagnosis_text,
            sources=list(unique_sources.values()),
            confidence="High based on RAG context"
        )
        
    except Exception as e:
        print(f"Error handling query: {e}")
        raise HTTPException(status_code=500, detail=str(e))
