from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime, timedelta
import pandas as pd
import random
import os
from dotenv import load_dotenv
import requests
from google.cloud import storage
from google.cloud import bigquery


# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
project_id = os.getenv('PROJECT_ID')
data_lakehouse_raw_bucket = os.getenv('DATA_LAKEHOUSE_RAW_BUCKET')
raw_stock_market_record_dataset = os.getenv('RAW_STOCK_MARKET_RECORD_DATASET')
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Function to test GCP authentication
def test_gcp_auth():
    credentials, project = google.auth.default()
    print(f"Authenticated with project: {project}")

#generating transactions
def generate_transactions():
    stock_list = ['AAPL', 'GOOG', 'TSLA', 'AMZN', 'MSFT']
    num_trades = 100
    start_date = datetime.now() - timedelta(days=365)
    data = []
    
    for _ in range(num_trades):
        trade = {
            'date': (start_date + timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
            'ticker': random.choice(stock_list),
            'quantity': random.randint(1, 10),
            'price': round(random.uniform(100, 500), 2),
            'type': random.choice(['BUY', 'SELL'])
        }
        data.append(trade)
    
    df = pd.DataFrame(data)
    local_path = '/tmp/transactions.csv'
    df.to_csv(local_path, index=False)
    
    # Upload to GCS
    client = storage.Client(project=project_id)
    bucket = client.bucket(data_lakehouse_raw_bucket)
    blob = bucket.blob('transactions.csv')
    blob.upload_from_filename(local_path)
    
    os.remove(local_path)

# Fetch stock data function
def fetch_stock_data():
    if not api_key:
        print("API key not found. Please set it in the .env file.")
        return
    
    symbols = ['AAPL', 'GOOG', 'TSLA', 'AMZN', 'MSFT']
    data = []
    
    for symbol in symbols:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize=compact'
        response = requests.get(url)
        stock_data = response.json()
        if 'Time Series (Daily)' in stock_data:
            for date, values in stock_data['Time Series (Daily)'].items():
                data.append({
                    'date': date,
                    'ticker': symbol,
                    'open': values['1. open'],
                    'high': values['2. high'],
                    'low': values['3. low'],
                    'close': values['4. close'],
                    'volume': values['5. volume']
                })
    
    df = pd.DataFrame(data)
    local_path = '/tmp/stock_data.csv'
    df.to_csv(local_path, index=False)
    
    # Upload to GCS
    client = storage.Client(project=project_id)
    bucket = client.bucket(data_lakehouse_raw_bucket)
    blob = bucket.blob('stock_data.csv')
    blob.upload_from_filename(local_path)
    
    os.remove(local_path)

with DAG('portfolio_tracker_pipeline', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    
    generate_task = PythonOperator(
        task_id='generate_transactions_csv',
        python_callable=generate_transactions
    )
    
    fetch_stock_task = PythonOperator(
        task_id='fetch_stock_data_csv',
        python_callable=fetch_stock_data
    )
    
    load_transactions_to_bq = GCSToBigQueryOperator(
        task_id='load_transactions_to_bq',
        bucket=data_lakehouse_raw_bucket,
        source_objects=['transactions.csv'],
        destination_project_dataset_table=f'{project_id}.{raw_stock_market_record_dataset}.transactions',
        write_disposition='WRITE_TRUNCATE',
        source_format='CSV',
        autodetect=True,
    )
    
    load_stock_data_to_bq = GCSToBigQueryOperator(
        task_id='load_stock_data_to_bq',
        bucket=data_lakehouse_raw_bucket,
        source_objects=['stock_data.csv'],
        destination_project_dataset_table=f'{project_id}.{raw_stock_market_record_dataset}.stock_data',
        write_disposition='WRITE_TRUNCATE',
        source_format='CSV',
        autodetect=True,
    )
    
    # Task dependencies
    generate_task >> load_transactions_to_bq
    fetch_stock_task >> load_stock_data_to_bq