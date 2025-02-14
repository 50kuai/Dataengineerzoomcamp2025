from pathlib import Path
import os
from os import getenv
import json
from airflow.models import Variable
from datetime import datetime, timedelta

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from ingest_script import ingest_callable


AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")


PG_HOST = Variable.get('PG_HOST', 'ingest-db')
PG_USER = os.getenv('PG_USER','postgres')
PG_PASSWORD = os.getenv('PG_PASSWORD','postgres')
PG_PORT = os.getenv('PG_PORT',5432)
PG_DATABASE = os.getenv('PG_DATABASE','nyc_taxi')

TABLE_NAME = 'yellow_taxi'
STAGING_TABLE = 'staging_yellow_taxi'

# Fetch years and months from Airflow Variables
BACKFILL_YEARS_MONTHS = json.loads(Variable.get("BACKFILL_YEARS_MONTHS", '{"years": [2019, 2020, 2021], "months": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}'))

# Define YEARS and MONTHS from the variable
YEARS = BACKFILL_YEARS_MONTHS['years']
MONTHS = BACKFILL_YEARS_MONTHS['months']

print(f"Years: {BACKFILL_YEARS_MONTHS}")



# Define default_args
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2021, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "Backfill_Yellow_Taxi",
    schedule="@once",
    default_args=default_args,
    catchup=False
) as dag:

    for year in YEARS:
        for month in MONTHS:
            # Define dataset URL dynamically
            dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_{year}-{month:02d}.csv.gz"

            # Define output file path dynamically
            output_file_path = f"/opt/airflow/{Path(dataset_url).name}"

            # Task: Download dataset
            wget_task = BashOperator(
                task_id=f"wget_{year}_{month}",
                bash_command=f"curl -sSL {dataset_url} > {output_file_path}"
            )

# Task: Ingest dataset into PostgreSQL
            ingest_task = PythonOperator(
                task_id=f"ingest_{year}_{month}",
                python_callable=ingest_callable,
                op_kwargs={
                    "user": PG_USER,
                    "password": PG_PASSWORD,
                    "host": PG_HOST,
                    "port": PG_PORT,
                    "db": PG_DATABASE,
                    "table_name": TABLE_NAME,
                    "csv_file": output_file_path  # Now it's correctly passed
                },
            )

    wget_task >> ingest_task