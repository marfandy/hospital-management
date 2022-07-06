import os
from passlib.hash import sha256_crypt
from flask import request, make_response, jsonify
from flask import Blueprint
from flask import Flask
from api.appointments import route as appointments
from api.auth import route as auth
from api.doctors import route as doctors
from api.employee import route as employee
from api.patients import route as patients
from common.database import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY', 'secret_key'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)
    db.create_all()
    app.register_blueprint(appointments, url_prefix='/appointments')
    app.register_blueprint(auth, url_prefix='/login')
    app.register_blueprint(doctors, url_prefix='/doctors')
    app.register_blueprint(employee, url_prefix='/employee')
    app.register_blueprint(patients, url_prefix='/patients')

    return app
