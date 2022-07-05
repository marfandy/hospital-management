from flask import Blueprint

route = Blueprint('auth', __name__)

@route.get('')
def hello():
    return "Hello from Home Page"
