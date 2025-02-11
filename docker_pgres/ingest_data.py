import os
import argparse
import pyarrow.csv as pv
import pandas as pd
from sqlalchemy import create_engine
from os import getenv

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url
    
    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    # Download the file
    os.system(f"wget {url} -O {csv_name}")

    # Create connection to the PostgreSQL database
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    # Use PyArrow to read the CSV directly into a PyArrow table
    table = pv.read_csv(csv_name)

    # Convert PyArrow table to pandas dataframe for further processing (if needed)
    df = table.to_pandas()

    # Insert the data directly into PostgreSQL
    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    print(f"Data successfully ingested into the {table_name} table in PostgreSQL.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', default=getenv("DB_USER"), required=False, help='user name for postgres')
    parser.add_argument('--password', default=getenv("DB_PASS"), required=False, help='password for postgres')
    parser.add_argument('--host', default=getenv("DB_HOST", "localhost"), required=False, help='host for postgres')
    parser.add_argument('--port', default=getenv("DB_PORT", 5432), required=False, help='port for postgres')
    parser.add_argument('--db', default=getenv("DB_NAME", "ny_taxi"), required=False, help='database name for postgres')
    parser.add_argument('--table_name', default=getenv("DB_TABLENAME"), required=False, help='name of the table where we will write the results to')
    parser.add_argument('--url', default=getenv("URL"), required=False, help='url of the csv file')

    args = parser.parse_args()

    main(args)
