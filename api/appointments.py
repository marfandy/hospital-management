import datetime

from flask_jwt_extended import jwt_required
from common.database import AppointmentStatus, Appointments, Patiens, UserType, Users, db
from common.helper import format_check, schedule_check
from flask import Blueprint
from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError

route = Blueprint('appointments', __name__)


@route.post('')
@jwt_required()
def register_appointment() -> dict:
    patient_id: int = request.json.get('patient_id')
    doctor_id: int = request.json.get('doctor_id')
    datetime_: datetime.datetime = request.json.get('datetime')
    status: AppointmentStatus = request.json.get('status')
    diagnose: str = request.json.get('diagnose')
    notes: str = request.json.get('notes')

    if status not in [data.value for data in AppointmentStatus]:
        return make_response(jsonify({"message": "invalid input status"}), 400)

    if not format_check(datetime_, '%Y-%m-%d %H:%M:%S'):
        return make_response(jsonify({"message": "invalid format date"}), 400)

    doctor = Users.query.filter(
        Users.id == doctor_id, Users.user_type == UserType.doctor).first()

    patient = Patiens.query.filter(Patiens.id == patient_id).first()

    if not doctor:
        return make_response(jsonify({"message": "doctor not found!"}), 400)

    if not patient:
        return make_response(jsonify({"message": "patient not found!"}), 400)

    validate = schedule_check(
        daterime_pick=datetime_,
        start_date=doctor.work_start_time,
        end_date=doctor.work_end_time
    )

    if not validate:
        return make_response(jsonify({"message": "doctor not in duty!"}), 400)

    if Appointments.query.filter(
        Appointments.datetime == datetime_,
        Appointments.doctor_id == doctor.id
    ).first() is not None:
        return make_response(jsonify({"message": "doctor in orders!"}), 400)

    appointment = Appointments(
        patient_id=patient.id,
        doctor_id=doctor.id,
        datetime=datetime.datetime.strptime(datetime_, '%Y-%m-%d %H:%M:%S'),
        status=status,
        diagnose=diagnose,
        notes=notes,
    )
    try:
        pass
        db.session.add(appointment)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return make_response(jsonify({"message": str(e)}), 400)

    response = {
        "id": appointment.id,
        "patient_id": appointment.patient_id,
        "doctor_id": appointment.doctor_id,
        "datetime": str(appointment.datetime),
        "status": appointment.status.value,
        "diagnose": appointment.diagnose,
        "notes ": appointment.notes,
    }

    return make_response(jsonify({"message": "appointment created", "data": response}), 201)


@route.get('')
@jwt_required()
def get_list_appointments() -> dict:
    appointment = Appointments.query.all()

    response = [{
        "id": data.id,
        "patient_id": data.patient_id,
        "doctor_id": data.doctor_id,
        "datetime": str(data.datetime),
        "status": data.status.value,
        "diagnose": data.diagnose,
        "notes ": data.notes,
    } for data in appointment]

    return make_response(jsonify({"message": "success", "data": response}), 200)


@ route.get('/<int:id>')
@ jwt_required()
def get_detail_appointment(id: int) -> dict:
    appointment = Appointments.query.filter(Appointments.id == id).first()

    if appointment:
        response = {
            "id": appointment.id,
            "patient_id": appointment.patient_id,
            "doctor_id": appointment.doctor_id,
            "datetime": str(appointment.datetime),
            "status": appointment.status.value,
            "diagnose": appointment.diagnose,
            "notes ": appointment.notes,
        }
        return make_response(jsonify({"message": "success", "data": response}), 200)

    return make_response(jsonify({"message": "appointment not found!"}), 400)


@ route.put('/<int:id>')
@ jwt_required()
def update_appointment(id: int) -> dict:
    patient_id: int = request.json.get('patient_id')
    doctor_id: int = request.json.get('doctor_id')
    datetime_: datetime.date = request.json.get('datetime')
    status: AppointmentStatus = request.json.get('status')
    diagnose: str = request.json.get('diagnose')
    notes: str = request.json.get('notes')

    appointment = Appointments.query.filter(Appointments.id == id).first()

    doctor = Users.query.filter(
        Users.id == doctor_id, Users.user_type == UserType.doctor).first()

    patient = Patiens.query.filter(Patiens.id == patient_id).first()

    if not doctor:
        return make_response(jsonify({"message": "doctor not found!"}), 400)

    if not patient:
        return make_response(jsonify({"message": "patient not found!"}), 400)

    validate = schedule_check(
        daterime_pick=datetime_,
        start_date=doctor.work_start_time,
        end_date=doctor.work_end_time
    )

    if not validate:
        return make_response(jsonify({"message": "doctor not in duty!"}), 400)

    in_order = Appointments.query.filter(
        Appointments.datetime == datetime_,
        Appointments.doctor_id == doctor.id
    ).first()

    if in_order is not None:
        if in_order.id != appointment.id:
            return make_response(jsonify({"message": "doctor in orders!"}), 400)

    if appointment:
        appointment.patient_id = patient_id
        appointment.doctor_id = doctor_id
        appointment.datetime = datetime.datetime.strptime(
            datetime_, '%Y-%m-%d %H:%M:%S')
        appointment.status = status
        appointment.diagnose = diagnose,
        appointment.notes = notes,
        try:
            db.session.add(appointment)
            db.session.commit()
        except BaseException as e:
            db.session.rollback()
            return make_response(jsonify({"message": str(e)}), 500)

        response = {
            "id": appointment.id,
            "patient_id": appointment.patient_id,
            "doctor_id": appointment.doctor_id,
            "datetime": str(appointment.datetime),
            "status": appointment.status.value,
            "diagnose": appointment.diagnose,
            "notes ": appointment.notes
        }

        return make_response(jsonify({"message": "appointment updated", "data": response}), 200)

    return make_response(jsonify({"message": "appointment not found!"}), 400)


@ route.delete('/<int:id>')
@ jwt_required()
def delete_appointment(id: int) -> dict:
    appointment = Appointments.query.filter(Appointments.id == id).first()
    if appointment:
        db.session.delete(appointment)
        db.session.commit()
        return make_response(jsonify({"message": "appointment deleted"}), 200)
    return make_response(jsonify({"message": "appointment not found!"}), 400)
