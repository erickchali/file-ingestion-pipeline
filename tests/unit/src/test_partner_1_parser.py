import os
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from src.partner_1_parser import parse_file, CSV_TO_SCHEMA, ALL_COLUMNS


@pytest.mark.unit
def test_csv_to_schema_mapping():
    """Test that CSV_TO_SCHEMA contains the expected mappings."""
    assert "member_nbr" in CSV_TO_SCHEMA
    assert CSV_TO_SCHEMA["member_nbr"] == "member_id"
    assert len(CSV_TO_SCHEMA) > 0


@pytest.mark.unit
def test_all_columns_list():
    """Test that ALL_COLUMNS contains the expected columns."""
    assert "member_id" in ALL_COLUMNS
    assert "referral_code" in ALL_COLUMNS
    assert len(ALL_COLUMNS) > 0


@pytest.mark.unit
@patch("src.partner_1_parser.upload_file_to_s3")
@patch("src.partner_1_parser.pd.read_csv")
@patch("src.partner_1_parser.Minio")
def test_parse_file(mock_minio, mock_read_csv, mock_upload, sample_partner_1_data):
    """Test the parse_file function with mocked dependencies."""
    # Setup mocks
    mock_minio_instance = MagicMock()
    mock_minio.return_value = mock_minio_instance
    mock_minio_instance.bucket_exists.return_value = True
    
    mock_read_csv.return_value = sample_partner_1_data
    
    # Mock file operations
    with patch("builtins.open", mock_open()) as mock_file:
        with patch("os.makedirs"):
            with patch("os.path.exists", return_value=True):
                # Call the function
                result = parse_file(
                    minio_endpoint="minio:9000",
                    minio_access_key="minioadmin",
                    minio_secret_key="minioadmin",
                    bucket="partner-1",
                    file_names=["test.csv"],
                    local_path="/tmp"
                )
    
    # Assertions
    assert result is not None
    assert mock_read_csv.called
    assert mock_upload.called
    
    # Verify the partner code was added
    args, _ = mock_upload.call_args
    assert "processed" in _
    assert _.get("processed") is True


# Need to define mock_open for file operations
def mock_open():
    file_mock = MagicMock()
    file_mock.__enter__.return_value = file_mock
    return MagicMock(return_value=file_mock)
