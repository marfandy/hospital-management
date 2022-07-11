import datetime

from flask_jwt_extended import jwt_required
from common.database import Patiens, db, Gender
from common.helper import format_check
from flask import Blueprint
from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError

route = Blueprint('patients', __name__)


@route.post('')
@jwt_required()
def register_patient() -> dict:
    name: str = request.json.get('name')
    no_ktp: int = request.json.get('no_ktp')
    address: str = request.json.get('address')
    gender: Gender = request.json.get('gender')
    birthdate: datetime.date = request.json.get('birthdate')

    if not name or name == "":
        return make_response(jsonify({"message": "input name is required"}), 400)

    if gender not in [data.value for data in Gender]:
        return make_response(jsonify({"message": "invalid input gender"}), 400)

    if not format_check(birthdate, '%Y-%m-%d'):
        return make_response(jsonify({"message": "invalid format date"}), 400)

    if Patiens.query.filter(Patiens.no_ktp == no_ktp).first() is not None:
        return make_response(jsonify({"message": "patient already registered"}), 400)

    patient = Patiens(
        name=name,
        gender=gender,
        birthdate=datetime.datetime.strptime(birthdate, '%Y-%m-%d'),
        no_ktp=no_ktp,
        address=address,
    )
    try:
        db.session.add(patient)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return make_response(jsonify({"message": str(e)}), 400)

    response = {
        "id": patient.id,
        "name": patient.name,
        "gender": patient.gender.value,
        "birthdate": str(patient.birthdate),
        "no_ktp": patient.no_ktp,
        "address": patient.address,
        "vaccine_type ": patient.vaccine_type,
        "vaccine_count ": patient.vaccine_count,
    }

    return make_response(jsonify({"message": "patient created", "data": response}), 201)


@route.get('')
@jwt_required()
def get_list_patients() -> dict:
    patients = Patiens.query.all()

    response = [{
        "id": data.id,
        "name": data.name,
        "gender": data.gender.value,
        "birthdate": str(data.birthdate),
        "no_ktp": data.no_ktp,
        "address": data.address,
        "vaccine_type ": data.vaccine_type,
        "vaccine_count ": data.vaccine_count,
    } for data in patients]

    return make_response(jsonify({"message": "success", "data": response}), 200)


@ route.get('/<int:id>')
@ jwt_required()
def get_detail_patient(id: int) -> dict:
    patient = Patiens.query.filter(Patiens.id == id).first()

    # print(patient.appointments)

    for data in patient.appointments:
        print(data.doctor_id)

    if patient:
        response = {
            'patient': {
                "id": patient.id,
                "name": patient.name,
                "gender": patient.gender.value,
                "birthdate": str(patient.birthdate),
                "no_ktp": patient.no_ktp,
                "address": patient.address,
                "vaccine_type ": patient.vaccine_type,
                "vaccine_count ": patient.vaccine_count,
            },
            'medical_history': [{
                "id": data.id,
                "doctor_id": data.doctor_id,
                "datetime": str(data.datetime),
                "status": data.status.value,
                "diagnose": data.diagnose,
                "notes": data.notes,
            } for data in patient.appointments]
        }
        return make_response(jsonify({"message": "success", "data": response}), 200)

    return make_response(jsonify({"message": "patient not found!"}), 400)


@ route.put('/<int:id>')
@ jwt_required()
def update_patient(id: int) -> dict:
    name: str = request.json.get('name')
    no_ktp: int = request.json.get('no_ktp')
    address: str = request.json.get('address')
    gender: Gender = request.json.get('gender')
    birthdate: datetime.date = request.json.get('birthdate')

    patient = Patiens.query.filter(Patiens.id == id).first()

    if patient:
        patient.name = name
        patient.gender = gender
        patient.birthdate = datetime.datetime.strptime(birthdate, '%Y-%m-%d')
        patient.no_ktp = no_ktp
        patient.address = address,
        try:
            db.session.add(patient)
            db.session.commit()
        except BaseException as e:
            db.session.rollback()
            return make_response(jsonify({"message": str(e)}), 500)

        response = {
            "id": patient.id,
            "name": patient.name,
            "gender": patient.gender.value,
            "birthdate": str(patient.birthdate),
            "no_ktp": patient.no_ktp,
            "address": patient.address,
            "vaccine_type ": patient.vaccine_type,
            "vaccine_count ": patient.vaccine_count,
        }

        return make_response(jsonify({"message": "patient updated", "data": response}), 200)

    return make_response(jsonify({"message": "patient not found!"}), 400)


@ route.delete('/<int:id>')
@ jwt_required()
def delete_patient(id: int) -> dict:
    patient = Patiens.query.filter(Patiens.id == id).first()
    if patient:
        db.session.delete(patient)
        db.session.commit()
        return make_response(jsonify({"message": "patient deleted"}), 200)
    return make_response(jsonify({"message": "patient not found!"}), 400)
