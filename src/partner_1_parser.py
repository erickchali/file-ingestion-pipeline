from typing import List
import os
import pandas as pd

from src.s3_helper import upload_file_to_s3

CSV_TO_SCHEMA = {
    "src_sys_mbr_id": "member_id",
    "enrl_from_dt": "benefit_start_date",
    "enrl_thru_dt": "benefit_end_date",
    "brth_dt": "dob",
    "first_nm": "first_name",
    "mid_nm": "middle_name",
    "last_nm": "last_name",
    "gend_cd": "gender",
    "address_ln_1": "address_line_1",
    "address_ln_2": "address_line_2",
    "city_nm": "city",
    "st_cd": "state",
    "pstl_cd": "zip_code",
    "phone_nbr": "primary_phone_number",
    "email_addr_txt": "email",
    "cob_type": "coverage_type"
}

ALL_COLUMNS = [
    "member_id", "referral_code", "benefit_start_date", "benefit_end_date", "dob",
    "first_name", "last_name", "middle_name", "gender", "address_line_1", "address_line_2",
    "city", "state", "zip_code", "primary_phone_number", "secondary_phone_number",
    "email", "coverage_type"
]

def parse_file(
    minio_endpoint: str,
    minio_access_key: str,
    minio_secret_key: str,
    local_path: str,
    file_names: List[str],
    bucket: str,
):
    processed_files = []
    for file_name in file_names:
        csv_path = os.path.join(local_path, file_name)
        df = pd.read_csv(csv_path)

        df = df.rename(columns=CSV_TO_SCHEMA)

        df["referral_code"] = "partner-1"
        df["benefit_start_date"] = pd.to_datetime(df["benefit_start_date"], errors="coerce")
        df["benefit_end_date"] = pd.to_datetime(df["benefit_end_date"], errors="coerce")
        df["dob"] = pd.to_datetime(df["dob"], errors="coerce").dt.date
        df["secondary_phone_number"] = ""

        df = df[ALL_COLUMNS]

        parquet_file_name = file_name.replace(".csv", ".parquet")
        parquet_path = os.path.join(local_path, parquet_file_name)
        df.to_parquet(parquet_path, index=False)
        print(f"Sanitized data written to {parquet_path}")
        processed_files.append(parquet_file_name)

    upload_file_to_s3(
        minio_endpoint=minio_endpoint,
        minio_access_key=minio_access_key,
        minio_secret_key=minio_secret_key,
        bucket=bucket,
        file_names=processed_files,
        local_path=local_path,
        processed=True
    )
