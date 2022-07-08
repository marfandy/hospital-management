import os
from app.config import GCP_OS
from google.cloud import bigquery


client = bigquery.Client()


def do_task():
    query = """
        SELECT 
            no_ktp, vaccine_type, vaccine_count
        FROM 
            `delman-interview.interview_mock_data.vaccine-data`
        """
    query_job = client.query(query)

    for row in query_job:
        no_ktp = row.get('no_ktp')
        vaccine_type = row.get('vaccine_type')
        vaccine_count = row.get('vaccine_count')
        print(no_ktp, vaccine_type, vaccine_count)
