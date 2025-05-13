import pendulum
import os

from airflow import DAG
from airflow.providers.sftp.hooks.sftp import SFTPHook
from airflow.providers.standard.operators.python import PythonOperator

from src.partner_1_parser import parse_file
from src.s3_helper import upload_file_to_s3
from src.sftp_helper import fetch_files_from_sftp


def download_files_from_sftp_task(**kwargs):
    downloaded_file_names = fetch_files_from_sftp(
        sftp_connection_id='sftp_partner1',
        sftp_directory='/download',
        local_directory='/tmp',
        partner_name='Partner One'
    )
    kwargs['ti'].xcom_push(key='downloaded_file_names', value=downloaded_file_names)

def backup_to_s3_task(**kwargs):
    ti = kwargs['ti']
    file_names = ti.xcom_pull(task_ids='download_file_from_sftp', key='downloaded_file_names')
    local_path = f"/tmp"
    bucket = "partner-1"

    upload_file_to_s3(
        minio_endpoint="minio:9000",
        minio_access_key="minioadmin",
        minio_secret_key="minioadmin",
        bucket=bucket,
        local_path=local_path,
        file_names=file_names
    )

def parse_file_task(**kwargs):
    ti = kwargs['ti']
    file_names = ti.xcom_pull(task_ids='download_file_from_sftp', key='downloaded_file_names')
    local_path = f"/tmp"
    bucket = "partner-1"
    parse_file(
        minio_endpoint="minio:9000",
        minio_access_key="minioadmin",
        minio_secret_key="minioadmin",
        local_path=local_path,
        file_names=file_names,
        bucket=bucket
    )

default_args = {
    'owner': 'MadFatKirby',
    'retries': 1,
}

with DAG(
    dag_id='partner1_etl',
    default_args=default_args,
    description='ETL pipeline for Partner 1 (dynamic filename)',
    schedule='0 6 * * 1',
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    tags=['partner1','etl','csv']
) as dag:
    download_file = PythonOperator(
        task_id='download_file_from_sftp',
        python_callable=download_files_from_sftp_task
    )
    
    backup_to_s3 = PythonOperator(
        task_id='backup_to_s3_task',
        python_callable=backup_to_s3_task
    )

    parse_partner_file = PythonOperator(
        task_id='parse_file_task',
        python_callable=parse_file_task
    )

    download_file >> backup_to_s3 >> parse_partner_file
