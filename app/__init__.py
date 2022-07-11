from flask import Flask, jsonify
from api.appointments import route as appointments
from api.auth import route as auth
from api.doctors import route as doctors
from api.employee import route as employee
from api.patients import route as patients
from common.database import db
from common.scheduler import cronjob
from flask_jwt_extended import JWTManager
from flask_apscheduler import APScheduler
from config.config import config_dict
from werkzeug.exceptions import NotFound, MethodNotAllowed
scheduler = APScheduler()


def create_app(config=config_dict['dev']):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    db.app = app
    db.init_app(app)

    db.create_all()

    JWTManager(app)

    app.register_blueprint(appointments, url_prefix='/appointments')
    app.register_blueprint(auth, url_prefix='/login')
    app.register_blueprint(doctors, url_prefix='/doctors')
    app.register_blueprint(employee, url_prefix='/employees')
    app.register_blueprint(patients, url_prefix='/patients')

    # add cronjob every day at 01:00
    @scheduler.task('cron', id='big_query', minute='*', hour="*")
    def running_cronjob():
        cronjob()

    # scheduler.start()
    try:
        scheduler.start()
    except Exception as e:
        print(e)
    scheduler.shutdown()
    print('done!')

    @app.errorhandler(NotFound)
    def handle_404(e):
        return jsonify({'message': 'not found!'}), 404

    @app.errorhandler(MethodNotAllowed)
    def handle_405(e):
        return jsonify({'message': 'method not allowed'}), 405

    return app
