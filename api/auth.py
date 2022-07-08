from flask import Blueprint, request, make_response, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash

from common.database import Users

route = Blueprint('auth', __name__)


@route.post('')
def login():
    username = request.json.get('username', '')
    password = request.json.get('password', '')

    user = Users.query.filter(Users.username == username).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            access = create_access_token(identity=user.id)
            refresh = create_refresh_token(identity=user.id)

            return make_response(jsonify({
                "access": access,
                "refresh": refresh,
                "name": user.name,
                "username": user.username,
            }))

        return make_response(jsonify({"message": "invalid password"}), 400)
    return make_response(jsonify({"message": "user not found!"}), 400)
