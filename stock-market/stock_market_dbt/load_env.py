from dotenv import load_dotenv
import os

load_dotenv()

# Add this line:
print(f"DBT_BIGQUERY_DATASET_LOCATION: {os.environ.get('DBT_BIGQUERY_DATASET_LOCATION')}")