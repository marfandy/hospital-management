from flask import Blueprint

route = Blueprint('doctor', __name__)


@route.get('')
def hello():
    return "Hello from Home Page"
