import os
import pandas as pd
import pytest
from unittest.mock import MagicMock, patch

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
        "member_nbr": ["12345", "67890"],
        "ref_cd": ["", ""],
        "benefit_start_dt": ["2023-01-01", "2023-02-01"],
        "benefit_end_dt": ["2023-12-31", "2023-12-31"],
        "birth_dt": ["1980-05-15", "1975-10-20"],
        "first_name": ["John", "Jane"],
        "last_name": ["Doe", "Smith"],
        "middle_name": ["", "M"],
        "gender_cd": ["M", "F"],
        "addr_line_1_txt": ["123 Main St", "456 Oak Ave"],
        "addr_line_2_txt": ["Apt 4B", ""],
        "city_name": ["Springfield", "Rivertown"],
        "state_cd": ["IL", "NY"],
        "pstl_cd": ["62701", "10001"],
        "phone_nbr": ["5551234567", "5559876543"],
        "email_addr_txt": ["john.doe@example.com", "jane.smith@example.com"],
        "cob_type": ["Primary", "Secondary"]
    }
    return pd.DataFrame(data)

@pytest.fixture
def airflow_context():
    """Mock Airflow context for DAG testing."""
    return {
        "ti": MagicMock(),
        "ds": "2025-05-25",
        "next_ds": "2025-05-26",
        "dag_run": MagicMock(),
    }
