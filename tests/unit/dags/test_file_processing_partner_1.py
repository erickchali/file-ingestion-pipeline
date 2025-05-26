import pytest
from unittest.mock import patch

from airflow.models import DagBag
from dags.file_processing_partner_1 import (
    download_files_from_sftp_task,
    backup_to_s3_task,
    parse_file_task,
)


@pytest.mark.unit
def test_dag_loaded():
    """Test that the DAG is correctly defined."""
    dag_bag = DagBag(include_examples=False)
    dag = dag_bag.get_dag(dag_id="partner1_etl")
    assert dag is not None
    assert dag.dag_id == "partner1_etl"
    assert len(dag.tasks) == 4


@pytest.mark.unit
def test_dag_structure():
    """Test the structure of the DAG and its dependencies."""
    dag_bag = DagBag(include_examples=False)
    dag = dag_bag.get_dag(dag_id="partner1_etl")

    task_ids = [task.task_id for task in dag.tasks]
    assert "download_file_from_sftp" in task_ids
    assert "backup_to_s3_task" in task_ids
    assert "parse_file_task" in task_ids
    assert "load_to_db_task" in task_ids

    backup_task = dag.get_task("backup_to_s3_task")
    parse_task = dag.get_task("parse_file_task")
    load_task = dag.get_task("load_to_db_task")

    assert backup_task.upstream_task_ids == {"download_file_from_sftp"}
    assert parse_task.upstream_task_ids == {"backup_to_s3_task"}
    assert load_task.upstream_task_ids == {"parse_file_task"}


@pytest.mark.unit
@patch("dags.file_processing_partner_1.upload_file_to_s3")
def test_backup_to_s3_task(mock_upload, airflow_context):
    """Test the backup_to_s3_task function."""
    ti = airflow_context["ti"]
    ti.xcom_pull.return_value = ["test.csv"]

    backup_to_s3_task(**airflow_context)

    assert ti.xcom_pull.called
    assert ti.xcom_pull.call_args[1]["task_ids"] == "download_file_from_sftp"
    assert mock_upload.called
    assert mock_upload.call_args[1]["bucket"] == "partner-1"


@pytest.mark.unit
@patch("dags.file_processing_partner_1.parse_file")
def test_parse_file_task(mock_parse, airflow_context):
    """Test the parse_file_task function."""
    ti = airflow_context["ti"]
    ti.xcom_pull.return_value = ["test.csv"]

    parse_file_task(**airflow_context)

    assert ti.xcom_pull.called
    assert mock_parse.called


@pytest.mark.unit
@patch("dags.file_processing_partner_1.fetch_files_from_sftp")
def test_download_files_from_sftp_task(mock_sftp, airflow_context):
    """Test the download_files_from_sftp_task function."""
    mock_sftp.return_value = ["test.csv"]
    ti = airflow_context["ti"]

    download_files_from_sftp_task(**airflow_context)

    assert mock_sftp.called
    assert ti.xcom_push.called
    assert ti.xcom_push.call_args[1]["key"] == "downloaded_file_names"
    assert ti.xcom_push.call_args[1]["value"] == ["test.csv"]
