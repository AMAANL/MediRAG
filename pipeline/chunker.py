import json
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
def load_and_chunk_data():
    """
    Loads JSON data from PubMed and openFDA, extracts text fields,
    and splits them into 512-token chunks with 50-token overlap.
    Returns a list of dictionaries with chunks and metadata.
    """
    pubmed_file = "data/raw/pubmed_articles.json"
    fda_file = "data/raw/fda_drugs.json"
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50,
        length_function=len
    )
    
    chunks = []
    
    if os.path.exists(pubmed_file):
        with open(pubmed_file, "r", encoding="utf-8") as f:
            pubmed_data = json.load(f)
            for item in pubmed_data:
                splits = text_splitter.split_text(item["abstract"])
                for i, split in enumerate(splits):
                    chunks.append({
                        "text": split,
                        "metadata": {
                            "source": item["source"],
                            "article_id": item["article_id"],
                            "title": item["title"],
                            "url": item["url"],
                            "chunk_index": i
                        }
                    })
                    
    if os.path.exists(fda_file):
        with open(fda_file, "r", encoding="utf-8") as f:
            fda_data = json.load(f)
            for item in fda_data:
                splits = text_splitter.split_text(item["description"])
                for i, split in enumerate(splits):
                    chunks.append({
                        "text": split,
                        "metadata": {
                            "source": item["source"],
                            "article_id": item["article_id"],
                            "title": item["title"],
                            "url": item["url"],
                            "chunk_index": i
                        }
                    })
                    
    print(f"Created {len(chunks)} total chunks.")
    return chunks
