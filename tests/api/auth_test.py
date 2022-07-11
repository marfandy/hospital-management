import unittest
from app import create_app
from config.config import config_dict
from common.database import Gender, UserType, Users, db
from werkzeug.security import generate_password_hash
import datetime


class AuthLoginTest(unittest.TestCase):

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
            name='test',
            username='test',
            password=generate_password_hash('test'),
            gender=Gender.male.value,
            birthdate=datetime.datetime.strptime("2021-01-01", '%Y-%m-%d'),
            user_type=UserType.employee
        )

        db.session.add(user)
        db.session.commit()

        return user

    def test_login_user_not_found(self):
        data = {
            "username": "test",
            "password": "test"
        }
        response = self.client.post('/login', json=data)

        assert response.status_code == 400
        assert response.json == {'message': 'user not found!'}

    def test_login_user_invalid_password(self):
        self.create_user()

        data = {
            "username": "test",
            "password": "xxxxx"
        }
        response = self.client.post('/login', json=data)

        assert response.status_code == 400
        assert response.json == {'message': 'invalid password'}

    def test_login_user(self):
        self.create_user()

        data = {
            "username": "test",
            "password": "test"
        }
        response = self.client.post('/login', json=data)

        assert response.status_code == 200
