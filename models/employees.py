from app.bootstrap import db
from datetime import datetime
import enum


class Gender(enum.Enum):
    male = "male"
    female = "female"


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum(Gender))

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False


db.create_all()
