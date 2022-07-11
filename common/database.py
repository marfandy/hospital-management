from datetime import datetime
import enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Gender(enum.Enum):
    male = "male"
    female = "female"


class UserType(enum.Enum):
    employee = "employee"
    doctor = "doctor"


class AppointmentStatus(enum.Enum):
    IN_QUEUE = "IN_QUEUE"
    DONE = "DONE"
    CANCELLED = "CANCELLED"


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.Enum(Gender))
    birthdate = db.Column(db.Date, nullable=False)
    work_start_time = db.Column(db.Time, nullable=True)
    work_end_time = db.Column(db.Time, nullable=True)
    user_type = db.Column(db.Enum(UserType))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return self.name


class Patiens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.Enum(Gender))
    birthdate = db.Column(db.Date, nullable=False)
    no_ktp = db.Column(db.BigInteger, unique=True, nullable=False)
    address = db.Column(db.String(75), nullable=False)
    vaccine_type = db.Column(db.String(20), nullable=True)
    vaccine_count = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    appointments = db.relationship('Appointments', backref='patiens')

    def __repr__(self) -> str:
        return self.name


class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patiens.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(AppointmentStatus))
    diagnose = db.Column(db.Text(), nullable=True)
    notes = db.Column(db.Text(), nullable=True)

    def __repr__(self) -> str:
        return self.status
