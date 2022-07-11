import datetime

from flask_jwt_extended import jwt_required
from common.database import UserType, Users, db, Gender
from common.helper import format_check
from flask import Blueprint
from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

route = Blueprint('employee', __name__)


@route.post('')
@jwt_required()
def register_employee() -> dict:
    name: str = request.json.get('name')
    username: str = request.json.get('username')
    password: str = request.json.get('password')
    gender: Gender = request.json.get('gender')
    birthdate: datetime.date = request.json.get('birthdate')

    if not name or name == "":
        return make_response(jsonify({"message": "input name is required"}), 400)

    if gender not in [data.value for data in Gender]:
        return make_response(jsonify({"message": "invalid input gender"}), 400)

    if len(password) < 6:
        return make_response(jsonify({"message": "min password 6"}), 400)

    if not format_check(birthdate, '%Y-%m-%d'):
        return make_response(jsonify({"message": "invalid format date"}), 400)

    if Users.query.filter(Users.username == username).first() is not None:
        return make_response(jsonify({"message": "Username already registered"}), 400)

    employee = Users(
        name=name,
        username=username,
        password=generate_password_hash(password),
        gender=gender,
        birthdate=datetime.datetime.strptime(birthdate, '%Y-%m-%d'),
        user_type=UserType.employee
    )
    try:
        db.session.add(employee)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return make_response(jsonify({"message": str(e)}), 400)

    response = {
        "id": employee.id,
        "name": employee.name,
        "username": employee.username,
        "password": employee.password,
        "gender": employee.gender.value,
        "birthdate": str(employee.birthdate),
    }

    return make_response(jsonify({"message": "employee created", "data": response}), 201)


@route.get('')
@jwt_required()
def get_list_employees() -> dict:
    employees = Users.query.filter(Users.user_type == UserType.employee)

    response = [{
        "id": data.id,
        "name": data.name,
        "username": data.username,
        "password": data.password,
        "gender": data.gender.value,
        "birthdate": str(data.birthdate),
    } for data in employees]

    return make_response(jsonify({"message": "success", "data": response}), 200)


@route.get('/<int:id>')
@jwt_required()
def get_detail_employee(id: int) -> dict:
    employee = Users.query.filter(
        Users.id == id, Users.user_type == UserType.employee).first()

    if employee:
        response = {
            "id": employee.id,
            "name": employee.name,
            "username": employee.username,
            "password": employee.password,
            "gender": employee.gender.value,
            "birthdate": str(employee.birthdate),
        }
        return make_response(jsonify({"message": "success", "data": response}), 200)

    return make_response(jsonify({"message": "employee not found!"}), 400)


@route.put('/<int:id>')
@jwt_required()
def update_employee(id: int) -> dict:
    name: str = request.json.get('name')
    username: str = request.json.get('username')
    password: str = request.json.get('password')
    gender: Gender = request.json.get('gender')
    birthdate: datetime.date = request.json.get('birthdate')

    employee = Users.query.filter(
        Users.id == id, Users.user_type == UserType.employee).first()

    if employee:
        employee.name = name
        employee.username = username
        employee.password = generate_password_hash(password),
        employee.gender = gender
        employee.birthdate = datetime.datetime.strptime(birthdate, '%Y-%m-%d'),

        try:
            db.session.add(employee)
            db.session.commit()
        except BaseException as e:
            db.session.rollback()
            return make_response(jsonify({"message": str(e)}), 500)

        response = {
            "id": employee.id,
            "name": employee.name,
            "username": employee.username,
            "password": employee.password,
            "gender": employee.gender.value,
            "birthdate": str(employee.birthdate),
        }

        return make_response(jsonify({"message": "employee updated", "data": response}), 200)

    return make_response(jsonify({"message": "employee not found!"}), 400)


@route.delete('/<int:id>')
@jwt_required()
def delete_employee(id: int) -> dict:
    employee = Users.query.filter(
        Users.id == id, Users.user_type == UserType.employee).first()
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return make_response(jsonify({"message": "employee deleted"}), 200)
    return make_response(jsonify({"message": "employee not found!"}), 400)
