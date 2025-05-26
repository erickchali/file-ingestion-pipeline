import pandas as pd
import pytest
from unittest.mock import MagicMock

from src.partner_1_parser import CSV_TO_SCHEMA


@pytest.fixture
def mock_minio_client():
    """Mock MinIO client for S3 operations."""
    mock_client = MagicMock()
    mock_client.bucket_exists.return_value = True
    return mock_client


@pytest.fixture
def sample_partner_1_data():
    """Sample data fixture for partner 1 format."""
    data = {
        "src_sys_mbr_id": ["12345", "67890"],
        "enrl_from_dt": ["2023-01-01", "2023-02-01"],
        "enrl_thru_dt": ["2023-12-31", "2023-12-31"],
        "brth_dt": ["1980-05-15", "1975-10-20"],
        "first_nm": ["John", "Jane"],
        "last_nm": ["Doe", "Smith"],
        "mid_nm": ["", "M"],
        "gend_cd": ["M", "F"],
        "address_ln_1": ["123 Main St", "456 Oak Ave"],
        "address_ln_2": ["Apt 4B", ""],
        "city_nm": ["Springfield", "Rivertown"],
        "st_cd": ["IL", "NY"],
        "pstl_cd": ["62701", "10001"],
        "phone_nbr": ["5551234567", "5559876543"],
        "email_addr_txt": ["john.doe@example.com", "jane.smith@example.com"],
        "cob_type": ["Primary", "Secondary"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_partner_1_data_sanitized(sample_partner_1_data):
    df = sample_partner_1_data.rename(columns=CSV_TO_SCHEMA)
    return df


@pytest.fixture
def airflow_context():
    """Mock Airflow context for DAG testing."""
    return {
        "ti": MagicMock(),
        "ds": "2025-05-25",
        "next_ds": "2025-05-26",
        "dag_run": MagicMock(),
    }
