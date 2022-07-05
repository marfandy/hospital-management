from flask import Blueprint

route = Blueprint('patients', __name__)


@route.get('')
def hello():
    return "Hello from Home Page"
