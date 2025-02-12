from pathlib import Path
import os
from os import getenv
from airflow.models import Variable
from datetime import datetime

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

local_workflow = DAG(
    "LocalIngestionDag",
    start_date=datetime(2021, 1, 1),
    schedule="@once",
    catchup=False
)


DATASET_URL = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz' 
OUTPUT_FILE_PATH = f"/opt/airflow/{Path(DATASET_URL).name}"
TABLE_NAME = 'yellow_taxi'

with local_workflow:
    wget_task = BashOperator(
        task_id='wget',
        bash_command=f'curl -sSL {DATASET_URL} > {OUTPUT_FILE_PATH}'
    )

    ingest_task = PythonOperator(
        task_id="ingest",
        python_callable=ingest_callable,
        op_kwargs=dict(
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT,
            db=PG_DATABASE,
            table_name=TABLE_NAME,
            csv_file=OUTPUT_FILE_PATH
        ),
    )

    wget_task >> ingest_task