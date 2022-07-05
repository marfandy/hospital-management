from flask import Blueprint

route = Blueprint('appointments', __name__)


@route.get('')
def hello():
    return "Hello from Home Page"
