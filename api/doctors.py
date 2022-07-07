import datetime
from common.database import Doctors, db, Gender
from common.format_check import format_check
from flask import Blueprint
from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

route = Blueprint('doctor', __name__)


@route.post('')
def register_doctor() -> dict:
    name: str = request.json.get('name')
    username: str = request.json.get('username')
    password: str = request.json.get('password')
    gender: Gender = request.json.get('gender')
    birthdate: datetime.date = request.json.get('birthdate')
    work_start_time: datetime.time = request.json.get('work_start_time')
    work_end_time: datetime.time = request.json.get('work_end_time')

    if not name or name == "":
        return make_response(jsonify({"message": "input name is required"}), 400)

    if gender not in [data.value for data in Gender]:
        return make_response(jsonify({"message": "invalid input gender"}), 400)

    if len(password) < 6:
        return make_response(jsonify({"message": "min password 6"}), 400)

    if not format_check(birthdate, '%Y-%m-%d'):
        return make_response(jsonify({"message": "invalid format date"}), 400)

    if not format_check(work_start_time, '%H:%M:%S'):
        return make_response(jsonify({"message": "invalid format date"}), 400)

    if not format_check(work_end_time, '%H:%M:%S'):
        return make_response(jsonify({"message": "invalid format date"}), 400)

    if work_start_time > work_end_time:
        return make_response(jsonify({"message": "start time should be lower than end time"}), 400)

    doctor = Doctors(
        name=name,
        username=username,
        password=generate_password_hash(password),
        gender=gender,
        birthdate=birthdate,
        work_start_time=work_start_time,
        work_end_time=work_end_time,
    )
    try:
        db.session.add(doctor)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({"message": "Username already registered"}), 400)

    response = {
        "id": doctor.id,
        "name": doctor.name,
        "username": doctor.username,
        "password": doctor.password,
        "gender": doctor.gender.value,
        "birthdate": str(doctor.birthdate),
        "work_start_time": str(doctor.work_start_time),
        "work_end_time": str(doctor.work_end_time),
    }

    return make_response(jsonify({"message": "doctor created", "data": response}), 201)


@route.get('')
def get_list_doctors() -> dict:
    doctors = Doctors.query.all()

    response = [{
        "id": data.id,
        "name": data.name,
        "username": data.username,
        "password": data.password,
        "gender": data.gender.value,
        "birthdate": str(data.birthdate),
        "work_start_time": str(data.work_start_time),
        "work_end_time": str(data.work_end_time),
    } for data in doctors]

    return make_response(jsonify({"message": "success", "data": response}), 200)


@route.get('/<int:id>')
def get_detail_doctor(id) -> dict:
    doctor = Doctors.query.get(id)
    print(doctor.work_start_time)

    if doctor:
        response = {
            "id": doctor.id,
            "name": doctor.name,
            "username": doctor.username,
            "password": doctor.password,
            "gender": doctor.gender.value,
            "birthdate": str(doctor.birthdate),
            "work_start_time": str(doctor.work_start_time),
            "work_end_time": str(doctor.work_end_time),
        }
        return make_response(jsonify({"message": "success", "data": response}), 200)

    return make_response(jsonify({"message": "doctor not found!"}), 404)


@route.put('/<int:id>')
def update_doctor(id) -> dict:
    name: str = request.json.get('name')
    username: str = request.json.get('username')
    password: str = request.json.get('password')
    gender: Gender = request.json.get('gender')
    birthdate: datetime.date = request.json.get('birthdate')
    work_start_time: datetime.time = request.json.get('work_start_time')
    work_end_time: datetime.time = request.json.get('work_end_time')

    doctor = Doctors.query.get(id)

    if doctor:
        doctor.name = name
        doctor.username = username
        doctor.password = generate_password_hash(password),
        doctor.gender = gender
        doctor.birthdate = birthdate
        doctor.work_start_time = work_start_time
        doctor.work_end_time = work_end_time

        try:
            db.session.add(doctor)
            db.session.commit()
        except BaseException as e:
            return make_response(jsonify({"message": str(e)}), 500)

        response = {
            "id": doctor.id,
            "name": doctor.name,
            "username": doctor.username,
            "password": doctor.password,
            "gender": doctor.gender.value,
            "birthdate": str(doctor.birthdate),
            "work_start_time": str(doctor.work_start_time),
            "work_end_time": str(doctor.work_end_time),
        }

        return make_response(jsonify({"message": "doctor updated", "data": response}), 200)

    return make_response(jsonify({"message": "doctor not found!"}), 404)


@route.delete('/<int:id>')
def delete_doctor(id) -> dict:
    doctor = Doctors.query.get(id)
    if doctor:
        db.session.delete(doctor)
        db.session.commit()
        return make_response(jsonify({"message": "doctor deleted"}), 200)
    return make_response(jsonify({"message": "doctor not found!"}), 404)
