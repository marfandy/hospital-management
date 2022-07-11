import unittest
from flask_jwt_extended import create_access_token
from app import create_app
from config.config import config_dict
from common.database import Appointments, Gender, Patiens, UserType, Users, db
from werkzeug.security import generate_password_hash
import datetime
import string
import random


class BigQUeryServiceTest(unittest.TestCase):

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

    def create_patient(self, ktp):
        patient = Patiens(
            name="name",
            gender="male",
            birthdate=datetime.datetime.strptime("2020-01-01", '%Y-%m-%d'),
            no_ktp=ktp,
            address="address",
        )

        return patient

    def test_running_service(self):
        patien1 = self.create_patient(51710321121200016)
        db.session.add(patien1)

        patien2 = self.create_patient(51710321121200018)
        db.session.add(patien2)

        db.session.commit()

        assert patien1.vaccine_type == None
        assert patien1.vaccine_count == None
        assert patien2.vaccine_type == None
        assert patien2.vaccine_count == None

        from common.scheduler import cronjob
        cronjob()
        assert patien1.vaccine_type != None
        assert patien1.vaccine_count != None
        assert patien2.vaccine_type != None
        assert patien2.vaccine_count != None
