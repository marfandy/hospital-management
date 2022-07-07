import datetime
from common.database import Employee, db, Gender
from common.format_check import format_check
from flask import Blueprint
from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

route = Blueprint('employee', __name__)


@route.post('')
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

    employee = Employee(
        name=name,
        username=username,
        password=generate_password_hash(password),
        gender=gender,
        birthdate=birthdate
    )
    try:
        db.session.add(employee)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({"message": "Username already registered"}), 400)

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
def get_list_employees() -> dict:
    employees = Employee.query.all()

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
def get_detail_employee(id: int) -> dict:
    employee = Employee.query.get(id)

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

    return make_response(jsonify({"message": "employee not found!"}), 404)


@route.put('/<int:id>')
def update_employee(id: int) -> dict:
    name: str = request.json.get('name')
    username: str = request.json.get('username')
    password: str = request.json.get('password')
    gender: Gender = request.json.get('gender')
    birthdate: datetime.date = request.json.get('birthdate')

    employee = Employee.query.get(id)

    if employee:
        employee.name = name
        employee.username = username
        employee.password = generate_password_hash(password),
        employee.gender = gender
        employee.birthdate = birthdate

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

    return make_response(jsonify({"message": "employee not found!"}), 404)


@route.delete('/<int:id>')
def delete_employee(id: int) -> dict:
    employee = Employee.query.get(id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return make_response(jsonify({"message": "employee deleted"}), 200)
    return make_response(jsonify({"message": "employee not found!"}), 404)
