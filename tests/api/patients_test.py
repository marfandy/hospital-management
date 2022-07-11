import unittest
from flask_jwt_extended import create_access_token
from app import create_app
from config.config import config_dict
from common.database import Gender, Patiens, db
import datetime
import string
import random


class PasientsTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config=config_dict['testing'])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.client = None

    def create_patient(self):
        user = Patiens(
            name="patient",
            gender=Gender.male.value,
            birthdate=datetime.datetime.strptime("2021-01-01", '%Y-%m-%d'),
            no_ktp=''.join(random.sample(string.digits, 10)),
            address="address",
        )

        db.session.add(user)
        db.session.commit()

        return user

    def test_register_patient(self):
        data = {
            "name": "pasien 5",
            "gender": "male",
            "birthdate": "1993-03-01",
            "no_ktp": 51710321121200017,
            "address": "dsadasdasda"
        }

        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        response = self.client.post('/patients', json=data, headers=header)
        data_response = response.json

        assert response.status_code == 201
        assert data.get("no_ktp") == data_response.get(
            "data").get("no_ktp")

    def test_register_patient_duplicate_id(self):
        user = self.create_patient()
        user.no_ktp = 51710321121200017
        db.session.add(user)
        db.session.commit()

        data = {
            "name": "pasien 5",
            "gender": "male",
            "birthdate": "1993-03-01",
            "no_ktp": 51710321121200017,
            "address": "dsadasdasda"
        }

        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        response = self.client.post('/patients', json=data, headers=header)

        assert response.status_code == 400
        assert response.json == {"message": "patient already registered"}

    def test_get_patients(self):
        self.create_patient()
        self.create_patient()

        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}
        user = Patiens.query.all()
        response = self.client.get('/patients', headers=header)

        assert response.status_code == 200
        assert len(user) == 2

    def test_get_detail_patient(self):
        user = self.create_patient()
        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}
        response = self.client.get(f"/patients/{user.id}", headers=header)
        data = response.json

        assert response.status_code == 200
        assert user.no_ktp == data.get("data").get("patient").get("no_ktp")

    def test_update_patient(self):
        user = self.create_patient()
        data = {
            "name": "pasien5",
            "gender": "male",
            "birthdate": "1993-03-01",
            "no_ktp": 51710321121200017,
            "address": "dsadasdasda"
        }
        token = create_access_token(identity='testuser')
        header = {'Authorization': f'Bearer {token}'}

        response = self.client.put(
            f"/patients/{user.id}", json=data, headers=header)

        update_user = Patiens.query.filter(Patiens.id == user.id).first()
        assert response.status_code == 200
        assert data.get("name") == update_user.name
        assert data.get("no_ktp") == update_user.no_ktp

    def test_delete_patient(self):
        user = self.create_patient()
        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        users = Patiens.query.all()
        assert len(users) == 1

        response = self.client.delete(f"/patients/{user.id}", headers=header)
        users = Patiens.query.all()
        assert response.status_code == 200
        assert len(users) == 0
