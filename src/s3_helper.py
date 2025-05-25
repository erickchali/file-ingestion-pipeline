import pendulum
from minio import Minio


def upload_file_to_s3(
    minio_endpoint,
    minio_access_key,
    minio_secret_key,
    bucket,
    local_path,
    file_names,
    processed: bool = False,
    **kwargs,
):
    client = Minio(
        minio_endpoint,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        secure=False,
    )
    found = client.bucket_exists(bucket)
    if not found:
        client.make_bucket(bucket)

    for file_name in file_names:
        print(f"Uploading {local_path} to {bucket}/{file_name}")
        local_file_path = f"{local_path}/{file_name}"

        # just to add more real-world requirements.
        current_date_str = pendulum.today().format("YYYYMMDD")
        bucket_key = f"{current_date_str}/{file_name}"
        if processed:
            bucket_key = f"{current_date_str}/processed/{file_name}"

        client.fput_object(bucket, bucket_key, local_file_path)
        print(f"Uploaded {local_path} to {bucket}/{bucket_key}")
