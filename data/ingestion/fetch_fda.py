import os
import json
import requests
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def fetch_fda_drugs():
    """
    Fetch drug labels from openFDA API relating to rare diseases.
    Saves the fetched labels to a JSON file.
    """
    print("Fetching openFDA drug labels...")
    url = 'https://api.fda.gov/drug/label.json'
    params = {
        'search': 'rare disease',
        'limit': 30
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = data.get('results', [])
        print(f"Found {len(results)} drug labels. Parsing...")
        
        drugs = []
        for idx, result in enumerate(results):
            try:
                title = result.get('openfda', {}).get('brand_name', ['Unknown Brand'])[0]
                description = result.get('description', [''])[0]
                indications = result.get('indications_and_usage', [''])[0]
                
                # Combine relevant text
                text_content = f"{description}\n\nIndications and Usage: {indications}"
                
                if text_content.strip() != "Indications and Usage:":
                    drugs.append({
                        "article_id": f"fda_{idx}",
                        "title": title,
                        "description": text_content,
                        "source": "openFDA",
                        "url": "https://api.fda.gov/drug/label.json"
                    })
            except Exception as e:
                print(f"Error parsing drug label: {e}")
                
        output_path = "data/raw/fda_drugs.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(drugs, f, indent=4)
            
        print(f"Successfully saved {len(drugs)} drug labels to {output_path}")
        
    except Exception as e:
        print(f"Failed to fetch from openFDA: {e}")

if __name__ == "__main__":
    fetch_fda_drugs()
