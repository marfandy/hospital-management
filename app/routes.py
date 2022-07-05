from flask import Blueprint

from api.appointments import route as appointments
from api.auth import route as auth
from api.doctors import route as doctors
from api.employee import route as employee
from api.patients import route as patients

routers = Blueprint('api', __name__)

routers.register_blueprint(appointments, url_prefix='/appointments')
routers.register_blueprint(auth, url_prefix='/login')
routers.register_blueprint(doctors, url_prefix='/doctors')
routers.register_blueprint(employee, url_prefix='/employee')
routers.register_blueprint(patients, url_prefix='/patients')
