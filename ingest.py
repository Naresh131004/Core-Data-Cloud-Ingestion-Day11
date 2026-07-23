import os
import json
import requests

BASE_DIR = "/opt/airflow/dags"
output_file = os.path.join(BASE_DIR, "extracted_transactions_1.json")

def extract_from_api():
    print("Starting API data extraction...")
    
    # Using your exact target endpoint
    url = "https://jsonplaceholder.typicode.com/posts"
    
    try:
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            # The API returns the exact raw JSON list structure
            raw_data = response.json()
            
            # Ensure the output directory exists and write the raw data as a JSON array
            os.makedirs(BASE_DIR, exist_ok=True)
            with open(output_file, "w") as f:
                json.dump(raw_data, f, indent=4)
                
            print(f"SUCCESS: Extracted {len(raw_data)} records to {output_file}")
        else:
            raise Exception(f"API request failed with status code: {response.status_code}")
            
    except Exception as e:
        print(f"ERROR: Extraction failed: {e}")
        raise

if __name__ == "__main__":
    extract_from_api()
