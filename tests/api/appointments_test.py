import unittest
from flask_jwt_extended import create_access_token
from app import create_app
from config.config import config_dict
from common.database import Appointments, Gender, Patiens, UserType, Users, db
from werkzeug.security import generate_password_hash
import datetime
import string
import random


class AppointmentTest(unittest.TestCase):

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

    def create_patien(self):
        patiens = Patiens(
            name="patient",
            gender=Gender.male.value,
            birthdate=datetime.datetime.strptime("2021-01-01", '%Y-%m-%d'),
            no_ktp=''.join(random.sample(string.digits, 10)),
            address="address",
        )

        db.session.add(patiens)
        db.session.commit()

        return patiens

    def create_doctor(self):
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

    def test_add_appointment(self):
        patien = self.create_patien()
        doctor = self.create_doctor()
        data = {
            "patient_id": patien.id,
            "doctor_id": doctor.id,
            "datetime": "2021-07-01 18:00:00",
            "status": "IN_QUEUE",
            "diagnose": "",
            "notes": ""
        }
        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        response = self.client.post('/appointments', json=data, headers=header)
        data_response = response.json
        assert response.status_code == 201
        assert data.get("patient_id") == data_response.get(
            "data").get("patient_id")
        assert data.get("doctor_id") == data_response.get(
            "data").get("doctor_id")

    def test_add_appointment_not_in_schedule(self):
        patien = self.create_patien()
        doctor = self.create_doctor()
        data = {
            "patient_id": patien.id,
            "doctor_id": doctor.id,
            "datetime": "2021-07-01 10:00:00",
            "status": "IN_QUEUE",
            "diagnose": "",
            "notes": ""
        }
        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        response = self.client.post('/appointments', json=data, headers=header)
        data_response = response.json
        assert response.status_code == 400
        assert data_response == {"message": "doctor not in duty!"}

    def test_add_appointment_doctor_in_order(self):
        patien1 = self.create_patien()
        patien2 = self.create_patien()
        doctor = self.create_doctor()
        data1 = {
            "patient_id": patien1.id,
            "doctor_id": doctor.id,
            "datetime": "2021-07-01 18:00:00",
            "status": "IN_QUEUE",
            "diagnose": "",
            "notes": ""
        }
        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        response1 = self.client.post(
            '/appointments', json=data1, headers=header)
        assert response1.status_code == 201

        data2 = {
            "patient_id": patien2.id,
            "doctor_id": doctor.id,
            "datetime": "2021-07-01 18:00:00",
            "status": "IN_QUEUE",
            "diagnose": "",
            "notes": ""
        }

        response2 = self.client.post(
            '/appointments', json=data2, headers=header)

        data_response = response2.json

        assert response2.status_code == 400
        assert data_response == {"message": "doctor in orders!"}

    def test_get_appointment(self):
        patien1 = self.create_patien()
        patien2 = self.create_patien()
        doctor = self.create_doctor()
        data1 = {
            "patient_id": patien1.id,
            "doctor_id": doctor.id,
            "datetime": "2021-07-01 18:00:00",
            "status": "IN_QUEUE",
            "diagnose": "",
            "notes": ""
        }
        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        response = self.client.post(
            '/appointments', json=data1, headers=header)

        assert response.status_code == 201

        data2 = {
            "patient_id": patien2.id,
            "doctor_id": doctor.id,
            "datetime": "2021-07-01 19:00:00",
            "status": "IN_QUEUE",
            "diagnose": "",
            "notes": ""
        }

        response = self.client.post(
            '/appointments', json=data2, headers=header)

        assert response.status_code == 201

        appointment = Appointments.query.all()
        assert len(appointment) == 2

    def test_get_detail_appointment(self):
        patien = self.create_patien()
        doctor = self.create_doctor()
        data = {
            "patient_id": patien.id,
            "doctor_id": doctor.id,
            "datetime": "2021-07-01 18:00:00",
            "status": "IN_QUEUE",
            "diagnose": "",
            "notes": ""
        }
        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        response = self.client.post(
            '/appointments', json=data, headers=header)

        appointment_id = response.json
        appointment_id = appointment_id.get('data').get('id')

        assert response.status_code == 201

        # response = self.clien.get()
        response = self.client.get(
            f"/appointments/{appointment_id}", headers=header)
        data_response = response.json
        assert response.status_code == 200
        assert data_response.get('data').get(
            'datetime') == data.get('datetime')

    def test_update_appointment(self):
        patien = self.create_patien()
        doctor = self.create_doctor()
        data = {
            "patient_id": patien.id,
            "doctor_id": doctor.id,
            "datetime": "2021-07-01 18:00:00",
            "status": "IN_QUEUE",
            "diagnose": "",
            "notes": ""
        }
        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        response = self.client.post(
            '/appointments', json=data, headers=header)

        appointment_id = response.json
        appointment_id = appointment_id.get('data').get('id')

        assert response.status_code == 201

        data_update = {
            "patient_id": patien.id,
            "doctor_id": doctor.id,
            "datetime": "2021-07-01 18:00:00",
            "status": "IN_QUEUE",
            "diagnose": "data update",
            "notes": "data update"
        }

        response = self.client.put(
            f"/appointments/{appointment_id}", json=data_update, headers=header)

        assert response.status_code == 200

        appointment = Appointments.query.filter(
            Appointments.id == appointment_id).first()
        assert appointment.diagnose == "data update"
        assert appointment.notes == "data update"

    def test_delete_appoinment(self):
        patien = self.create_patien()
        doctor = self.create_doctor()
        data = {
            "patient_id": patien.id,
            "doctor_id": doctor.id,
            "datetime": "2021-07-01 18:00:00",
            "status": "IN_QUEUE",
            "diagnose": "",
            "notes": ""
        }
        token = create_access_token(identity='testuser')

        header = {'Authorization': f'Bearer {token}'}

        response = self.client.post(
            '/appointments', json=data, headers=header)

        appointment_id = response.json
        appointment_id = appointment_id.get('data').get('id')

        count_appoinment = Appointments.query.all()

        assert response.status_code == 201
        assert len(count_appoinment) == 1

        response = self.client.delete(
            f"/appointments/{appointment_id}", headers=header)

        count_appoinment = Appointments.query.all()

        assert response.status_code == 200
        assert len(count_appoinment) == 0
