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
from flask_jwt_extended import JWTManager
from common.scheduler import do_task
from flask_apscheduler import APScheduler


scheduler = APScheduler()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY', 'secret_key'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)
    db.create_all()

    JWTManager(app)

    app.register_blueprint(appointments, url_prefix='/appointments')
    app.register_blueprint(auth, url_prefix='/login')
    app.register_blueprint(doctors, url_prefix='/doctors')
    app.register_blueprint(employee, url_prefix='/employee')
    app.register_blueprint(patients, url_prefix='/patients')

    scheduler.add_job(
        id='Scheduled job',
        func=do_task,
        trigger='interval',
        # seconds=86400
        seconds=60
    )
    scheduler.start()

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({'message': 'not found!'}), 404
    return app