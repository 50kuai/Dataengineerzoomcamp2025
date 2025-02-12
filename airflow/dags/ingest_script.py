import os
import pyarrow.csv as pv
import pandas as pd
from sqlalchemy import create_engine

def ingest_callable(user, password, host, port, db, table_name, csv_file):

    # Create connection to the PostgreSQL database
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    print("Connection to PostgreSQL database successful.")

    print(f"Ingesting data from {csv_file} into {table_name}.")
    # Read CSV using PyArrow
    df=pd.read_csv(csv_file,engine='pyarrow')

    print(f"Data successfully read from {csv_file}.")
    # Insert the data into PostgreSQL
    try:
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)  # Use append instead of replace
    except Exception as e:
        print(e)
    print(f"Data successfully ingested into {table_name}.")

