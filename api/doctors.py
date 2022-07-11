import datetime

from flask_jwt_extended import jwt_required
from common.database import UserType, Users, db, Gender
from common.helper import format_check
from flask import Blueprint
from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

route = Blueprint('doctor', __name__)


@route.post('')
@jwt_required()
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

    if Users.query.filter(Users.username == username).first() is not None:
        return make_response(jsonify({"message": "Username already registered"}), 400)

    doctor = Users(
        name=name,
        username=username,
        password=generate_password_hash(password),
        gender=gender,
        birthdate=datetime.datetime.strptime(birthdate, '%Y-%m-%d'),
        work_start_time=datetime.datetime.strptime(
            work_start_time, '%H:%M:%S').time(),
        work_end_time=datetime.datetime.strptime(
            work_end_time, '%H:%M:%S').time(),
        user_type=UserType.doctor
    )
    try:
        db.session.add(doctor)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return make_response(jsonify({"message": str(e)}), 400)

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
@jwt_required()
def get_list_doctors() -> dict:
    doctors = Users.query.filter(Users.user_type == UserType.doctor)

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
@jwt_required()
def get_detail_doctor(id) -> dict:
    doctor = Users.query.filter(
        Users.id == id, Users.user_type == UserType.doctor).first()

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

    return make_response(jsonify({"message": "doctor not found!"}), 400)


@route.put('/<int:id>')
@jwt_required()
def update_doctor(id) -> dict:
    name: str = request.json.get('name')
    username: str = request.json.get('username')
    password: str = request.json.get('password')
    gender: Gender = request.json.get('gender')
    birthdate: datetime.date = request.json.get('birthdate')
    work_start_time: datetime.time = request.json.get('work_start_time')
    work_end_time: datetime.time = request.json.get('work_end_time')

    doctor = Users.query.filter(
        Users.id == id, Users.user_type == UserType.doctor).first()

    if doctor:
        doctor.name = name
        doctor.username = username
        doctor.password = generate_password_hash(password),
        doctor.gender = gender
        doctor.birthdate = datetime.datetime.strptime(birthdate, '%Y-%m-%d')
        doctor.work_start_time = datetime.datetime.strptime(
            work_start_time, '%H:%M:%S').time()
        doctor.work_end_time = datetime.datetime.strptime(
            work_end_time, '%H:%M:%S').time()

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

    return make_response(jsonify({"message": "doctor not found!"}), 400)


@route.delete('/<int:id>')
@jwt_required()
def delete_doctor(id) -> dict:
    doctor = Users.query.filter(
        Users.id == id, Users.user_type == UserType.doctor).first()
    if doctor:
        db.session.delete(doctor)
        db.session.commit()
        return make_response(jsonify({"message": "doctor deleted"}), 200)
    return make_response(jsonify({"message": "doctor not found!"}), 400)
