import unittest
from flask_jwt_extended import create_access_token
from app import create_app
from config.config import config_dict
from common.database import Gender, UserType, Users, db
from werkzeug.security import generate_password_hash
import datetime
import string
import random


class EmployeeTest(unittest.TestCase):

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
            name='employee',
            username=''.join(random.sample(string.ascii_letters, 10)),
            password=generate_password_hash('employee'),
            gender=Gender.male.value,
            birthdate=datetime.datetime.strptime("2021-01-01", '%Y-%m-%d'),
            user_type=UserType.employee
        )

        db.session.add(user)
        db.session.commit()

        return user

    def test_register_employee(self):
        data = {
            "name": "employee",
            "username": "employee",
            "password": "employee",
            "gender": "female",
            "birthdate": "2022-01-01"
        }

        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        response = self.client.post('/employee', json=data, headers=header)

        assert response.status_code == 201

    def test_get_employees(self):

        self.create_user()
        self.create_user()

        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        user = Users.query.all()

        response = self.client.get('/employee', headers=header)

        assert response.status_code == 200
        assert len(user) == 2

    def test_get_detail_employees(self):

        user = self.create_user()

        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        users = Users.query.all()

        response = self.client.get(f"/employee/{user.id}", headers=header)

        assert response.status_code == 200
        assert len(users) == 1
