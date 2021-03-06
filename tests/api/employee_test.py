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

        response = self.client.post('/employees', json=data, headers=header)
        data_response = response.json
        assert response.status_code == 201
        assert data.get("username") == data_response.get(
            "data").get("username")

    def test_register_employee_username_already_registed(self):
        user = self.create_user()
        user.username = 'employee'
        db.session.add(user)
        db.session.commit()

        data = {
            "name": "employee",
            "username": "employee",
            "password": "employee",
            "gender": "female",
            "birthdate": "2022-01-01"
        }

        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        response = self.client.post('/employees', json=data, headers=header)

        assert response.status_code == 400
        assert response.json == {"message": "Username already registered"}

    def test_get_employees(self):

        self.create_user()
        self.create_user()

        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        user = Users.query.all()

        response = self.client.get('/employees', headers=header)

        assert response.status_code == 200
        assert len(user) == 2

    def test_get_detail_employee(self):

        user = self.create_user()

        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        response = self.client.get(f"/employees/{user.id}", headers=header)
        data = response.json

        assert response.status_code == 200
        assert user.username == data.get("data").get('username')

    def test_update_employee(self):

        user = self.create_user()

        data = {
            "name": "newemployee",
            "username": "newemployee",
            "password": "employee",
            "gender": "male",
            "birthdate": "2000-01-01"
        }

        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        response = self.client.put(
            f"/employees/{user.id}", json=data, headers=header)

        update_user = Users.query.filter(Users.id == user.id).first()

        assert response.status_code == 200
        assert data.get("name") == update_user.name
        assert data.get("username") == update_user.username

    def test_delete_employee(self):

        user = self.create_user()

        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        users = Users.query.all()
        assert len(users) == 1

        response = self.client.delete(f"/employees/{user.id}", headers=header)

        users = Users.query.all()

        assert response.status_code == 200
        assert len(users) == 0
