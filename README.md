# Airflow Docker Compose Local Development

This project uses the official [Apache Airflow Docker Compose setup for local development](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#running-airflow-in-docker).

## Quick Start Instructions

1. **Create your `.env` file**
   - You can either rename `.env.example` to `.env`, or generate it using the command from the official docs:
     ```bash
     echo -e "AIRFLOW_UID=$(id -u)" > .env
     ```
   - See [Setting the right Airflow user](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#setting-the-right-airflow-user) for why this is important (avoids permission issues, specially on Linux).

2. **Initialize Airflow metadata database**
   ```bash
   docker compose -f docker-compose.yaml -f docker-compose.override.yaml up airflow-init
   ```

3. **Start all Airflow and custom services**
   ```bash
   docker compose -f docker-compose.yaml -f docker-compose.override.yaml up
   ```

   - This will launch the default Airflow stack along with your custom SFTP and Minio services defined in `docker-compose.override.yaml`.

At this point, everything should work as expected with the default Airflow Docker Compose setup plus your local extensions.

## Notes
- The `docker-compose.yaml` file at this stage is a direct implementation from the [official Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#running-airflow-in-docker) for local development.
- The `docker-compose.override.yaml` file contains custom services (SFTP servers, Minio, etc.) for local ETL pipeline development (this is what I really did).
- The `airflow-python` service exists only to provide a Python interpreter for debugging DAG code in PyCharm (as recommended in the official docs). It is not required for running Airflow itself.

---

If you need to customize the setup or encounter issues, consult the [Airflow Docker Compose docs](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html).
