import os
from flask import Blueprint
from flask import request, make_response, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from common.database import Employee, db

route = Blueprint('employee', __name__)


@route.post('')
def register_employee():
    name = request.json['name']
    username = request.json['username']
    password = request.json['password']
    gender = request.json['gender']
    birthdate = request.json['birthdate']

    if Employee.query.filter_by(username=username).first() is not None:
        return make_response(jsonify({"message": "Username already registered"}), 400)

    pwd_hash = generate_password_hash(password)

    employee = Employee(
        name=name,
        username=username,
        password=pwd_hash,
        gender=gender,
        birthdate=birthdate
    )
    db.session.add(employee)
    db.session.commit()

    response = {
        "id": employee.id,
        "name": employee.name,
        "username": employee.username,
        "password": employee.password,
        "gender": employee.gender.value,
        "birthdate": employee.birthdate,
    }

    return make_response(jsonify({"message": "employee created", "data": response}), 201)


@route.get('')
def get_list_employees():
    employees = Employee.query.all()

    response = [{
        "id": data.id,
        "name": data.name,
        "username": data.username,
        "password": data.password,
        "gender": data.gender.value,
        "birthdate": data.birthdate,
    } for data in employees]

    print(response)
    return make_response(jsonify({"message": "employee created", "data": response}), 200)
