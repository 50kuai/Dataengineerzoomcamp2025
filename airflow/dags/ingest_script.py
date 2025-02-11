import os
import pyarrow.csv as pv
import pandas as pd
from sqlalchemy import create_engine

def ingest_callable(user, password, host, port, db, table_name, csv_url):
    # Determine file name
    csv_name = "output.csv.gz" if csv_url.endswith('.csv.gz') else "output.csv"

    # Download the file
    os.system(f"wget {csv_url} -O {csv_name}")

    # Create connection to the PostgreSQL database
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    # Read CSV using PyArrow
    table = pv.read_csv(csv_name)
    df = table.to_pandas()

    # Insert the data into PostgreSQL
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)  # Use append instead of replace
    print(f"Data successfully ingested into {table_name}.")

