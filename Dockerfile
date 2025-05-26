FROM apache/airflow:3.0.0
ADD requirements.txt .
ADD pyproject.toml .
RUN pip install apache-airflow==3.0.0 -r requirements.txt