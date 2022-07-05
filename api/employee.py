from flask import Blueprint
from flask import request, make_response, jsonify
from app.config import gcp_os


route = Blueprint('employee', __name__)


@route.get('')
def hello():
    print(gcp_os)

    return make_response(jsonify({"message": "User not found!"}), 400)
