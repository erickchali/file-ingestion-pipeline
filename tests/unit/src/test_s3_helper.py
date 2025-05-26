import pytest
from unittest.mock import patch, MagicMock

from src.s3_helper import upload_file_to_s3


@pytest.mark.unit
@patch("src.s3_helper.Minio")
@patch("src.s3_helper.pendulum.today")
def test_upload_file_to_s3(mock_today, mock_minio, mock_minio_client):
    """Test the upload_file_to_s3 function."""
    # Setup mocks
    mock_minio.return_value = mock_minio_client
    mock_today_instance = MagicMock()
    mock_today_instance.format.return_value = "20250525"
    mock_today.return_value = mock_today_instance
    
    # Call the function
    upload_file_to_s3(
        minio_endpoint="minio:9000",
        minio_access_key="minioadmin",
        minio_secret_key="minioadmin",
        bucket="test-bucket",
        local_path="/tmp",
        file_names=["test1.csv", "test2.csv"]
    )
    
    # Assertions
    assert mock_minio.called
    assert mock_minio_client.bucket_exists.called
    assert mock_minio_client.fput_object.call_count == 2
    
    # Verify the date formatting and bucket path
    _, kwargs = mock_minio_client.fput_object.call_args_list[0]
    assert "20250525" in kwargs.get("object_name", "")


@pytest.mark.unit
@patch("src.s3_helper.Minio")
@patch("src.s3_helper.pendulum.today")
def test_upload_file_to_s3_processed(mock_today, mock_minio, mock_minio_client):
    """Test the upload_file_to_s3 function with processed=True flag."""
    # Setup mocks
    mock_minio.return_value = mock_minio_client
    mock_today_instance = MagicMock()
    mock_today_instance.format.return_value = "20250525"
    mock_today.return_value = mock_today_instance
    
    # Call the function with processed=True
    upload_file_to_s3(
        minio_endpoint="minio:9000",
        minio_access_key="minioadmin",
        minio_secret_key="minioadmin",
        bucket="test-bucket",
        local_path="/tmp",
        file_names=["test1.csv"],
        processed=True
    )
    
    # Assert that the processed path was used
    _, kwargs = mock_minio_client.fput_object.call_args
    assert "processed" in kwargs.get("object_name", "")
    assert "20250525/processed/" in kwargs.get("object_name", "")
