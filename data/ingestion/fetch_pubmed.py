import os
import json
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Bio import Entrez

def fetch_pubmed_articles():
    """
    Fetch articles from PubMed Entrez API relating to rare disease diagnosis.
    Saves the fetched articles to a JSON file.
    """
    print("Fetching PubMed articles...")
    Entrez.email = "example@example.com"  # Set your email
    search_term = "rare disease diagnosis treatment"
    
    try:
        # Search for IDs
        handle = Entrez.esearch(db="pubmed", term=search_term, retmax=50)
        record = Entrez.read(handle)
        handle.close()
        
        id_list = record["IdList"]
        print(f"Found {len(id_list)} articles. Fetching details...")
        
        # Fetch details
        handle = Entrez.efetch(db="pubmed", id=id_list, retmode="xml")
        records = Entrez.read(handle)
        handle.close()
        
        articles = []
        for pmid, pubmed_article in zip(id_list, records['PubmedArticle']):
            try:
                article = pubmed_article['MedlineCitation']['Article']
                title = article['ArticleTitle']
                abstract_text = ""
                if 'Abstract' in article and 'AbstractText' in article['Abstract']:
                    abstract_parts = article['Abstract']['AbstractText']
                    abstract_text = " ".join([str(part) for part in abstract_parts])
                
                if abstract_text: # only add if abstract exists
                    articles.append({
                        "article_id": pmid,
                        "title": title,
                        "abstract": abstract_text,
                        "source": "PubMed",
                        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                    })
            except Exception as e:
                print(f"Error parsing article {pmid}: {e}")
                
        output_path = "data/raw/pubmed_articles.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(articles, f, indent=4)
            
        print(f"Successfully saved {len(articles)} articles to {output_path}")
        
    except Exception as e:
        print(f"Failed to fetch from PubMed: {e}")

if __name__ == "__main__":
    fetch_pubmed_articles()
