from typing import List

from config.config import Config
from google.cloud import bigquery
from flask_crontab import Crontab
from common.database import Patiens, db

client = bigquery.Client()

crontab = Crontab()


class BigqueryService:
    def __init__(self):
        pass

    def update_data_patients(self, limit: int = 100, temp_data: List[dict] = []):

        print("===================")
        query = """
            SELECT
                no_ktp, vaccine_type, vaccine_count
            FROM
                `delman-interview.interview_mock_data.vaccine-data`
            """ + f'LIMIT {limit}'

        query_job = client.query(query)

        query_result = query_job.result()

        final_data = temp_data
        for data in query_result:
            new = {
                'no_ktp': data.get('no_ktp'),
                'vaccine_count': data.get('vaccine_count'),
                'vaccine_type': data.get('vaccine_type'),
            }

            final_data.append(new)

        print(query_result.total_rows)
        if query_result.total_rows == limit:
            temp_data = final_data
            self.update_data_patients(limit=limit+100, temp_data=temp_data)

        for data in final_data:
            no_ktp = data.get('no_ktp')
            vaccine_type = data.get('vaccine_type')
            vaccine_count = data.get('vaccine_count')

            print(no_ktp, vaccine_type, vaccine_count)

            patiens = Patiens.query.filter(Patiens.no_ktp == no_ktp).first()
            if patiens:
                patiens.vaccine_type = vaccine_type
                patiens.vaccine_count = vaccine_count
                db.session.add(patiens)
                db.session.commit()


service = BigqueryService()


@crontab.job(minute="*", hour="*", day="*")
def cronjob():
    service.update_data_patients(limit=100, temp_data=[])
