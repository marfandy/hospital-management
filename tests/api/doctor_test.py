import unittest
from flask_jwt_extended import create_access_token
from app import create_app
from config.config import config_dict
from common.database import Gender, UserType, Users, db
from werkzeug.security import generate_password_hash
import datetime
import string
import random


class DoctorTest(unittest.TestCase):

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

    def create_user(self):
        user = Users(
            name='doctor',
            username=''.join(random.sample(string.ascii_letters, 10)),
            password=generate_password_hash('doctor'),
            gender=Gender.male.value,
            birthdate=datetime.datetime.strptime("2021-01-01", '%Y-%m-%d'),
            user_type=UserType.doctor,
            work_start_time=datetime.datetime.strptime(
                "18:00:00", '%H:%M:%S').time(),
            work_end_time=datetime.datetime.strptime(
                "20:00:00", '%H:%M:%S').time()
        )

        db.session.add(user)
        db.session.commit()

        return user

    def test_register_doctor(self):
        data = {
            "name": "doctor",
            "username": "doctor",
            "password": "doctor",
            "gender": "male",
            "birthdate": "1993-03-01",
            "work_start_time": "18:00:00",
            "work_end_time": "20:00:00"
        }

        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        response = self.client.post('/doctors', json=data, headers=header)
        data_response = response.json

        assert response.status_code == 201
        assert data.get("username") == data_response.get(
            "data").get("username")

    def test_register_doctor_username_already_registed(self):
        user = self.create_user()
        user.username = 'doctor'
        db.session.add(user)
        db.session.commit()

        data = {
            "name": "doctor",
            "username": "doctor",
            "password": "doctor",
            "gender": "male",
            "birthdate": "1993-03-01",
            "work_start_time": "18:00:00",
            "work_end_time": "20:00:00"
        }

        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        response = self.client.post('/doctors', json=data, headers=header)

        assert response.status_code == 400
        assert response.json == {"message": "Username already registered"}

    def test_get_doctors(self):

        self.create_user()
        self.create_user()

        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        user = Users.query.all()

        response = self.client.get('/doctors', headers=header)

        assert response.status_code == 200
        assert len(user) == 2

    def test_get_detail_doctor(self):

        user = self.create_user()

        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        response = self.client.get(f"/doctors/{user.id}", headers=header)
        data = response.json

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.username, data.get("data").get('username'))

    def test_update_doctor(self):

        user = self.create_user()

        data = {
            "name": "newdoctor",
            "username": "newdoctor",
            "password": "doctor",
            "gender": "male",
            "birthdate": "2000-01-01",
            "work_start_time": "08:00:00",
            "work_end_time": "10:00:00"
        }

        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        response = self.client.put(
            f"/doctors/{user.id}", json=data, headers=header)

        update_user = Users.query.filter(Users.id == user.id).first()

        assert response.status_code == 200
        assert data.get("name") == update_user.name
        assert data.get("username") == update_user.username

    def test_delete_doctor(self):

        user = self.create_user()

        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        users = Users.query.all()
        assert len(users) == 1

        response = self.client.delete(f"/doctors/{user.id}", headers=header)

        users = Users.query.all()

        assert response.status_code == 200
        assert len(users) == 0
