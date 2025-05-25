from airflow.providers.sftp.hooks.sftp import SFTPHook


def fetch_files_from_sftp(
    sftp_connection_id: str,
    sftp_directory: str,
    local_directory: str,
    partner_name: str,
):
    sftp_hook = SFTPHook(ssh_conn_id=sftp_connection_id)
    files = sftp_hook.list_directory(sftp_directory)
    file_names = [f for f in files if not f.startswith(".")]
    if not file_names:
        raise ValueError(f"No files found for partner {partner_name} {sftp_directory}")

    for file_name in files:
        remote_path = f"{sftp_directory}/{file_name}"
        local_path = f"{local_directory}/{file_name}"
        sftp_hook.retrieve_file(remote_path, local_path)
    return file_names
