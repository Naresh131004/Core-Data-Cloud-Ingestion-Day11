import os
import boto3
from botocore.exceptions import NoCredentialsError

BASE_DIR = "/opt/airflow/dags" # or your local path if running outside docker
local_file = os.path.join(BASE_DIR, "extracted_transactions_1.json")

BUCKET_NAME = "de-bronze-api-ingestion-naresh"
S3_KEY = "raw/year=2026/month=07/day=14/extracted_transactions_1.json"

def upload_to_s3():
    print("Initializing AWS S3 upload client...")
    
    # Explicitly providing your keys here avoids any environment variable or configuration errors
    s3_client = boto3.client(
        's3',
        aws_access_key_id='YOUR AWS ACCESS KEY',
        aws_secret_access_key='YOUR AWS SECRET ACCESS KEY',
        region_name='ap-south-1'
    )
    
    try:
        if not os.path.exists(local_file):
            raise FileNotFoundError(f"Local file not found at {local_file}")
            
        s3_client.upload_file(local_file, BUCKET_NAME, S3_KEY)
        print(f"SUCCESS: Uploaded to s3://{BUCKET_NAME}/{S3_KEY}")
        
    except NoCredentialsError:
        print("ERROR: AWS credentials are invalid or missing.")
        raise
    except Exception as e:
        print(f"ERROR: S3 upload failed: {e}")
        raise

if __name__ == "__main__":
    upload_to_s3()
