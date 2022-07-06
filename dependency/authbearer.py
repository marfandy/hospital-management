import datetime
import jwt

from app.config import configs
from functools import wraps
from flask import request, make_response, jsonify


class TokenBearer():
    def __init__(self) -> None:
        pass

    def create_token(self, data: str) -> dict:

        token = jwt.encode(
            {
                "username": data.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }, configs.secret_key, algorithm="HS256"
        )
        return jsonify({
            "token": token
        })

    def token_required(self, f):
        @wraps(f)
        def decorator(*args, **kwargs):
            token = request.headers.get('token')

            if not token:
                return make_response(jsonify({"message": "Invalid Token!"}), 400)
            try:
                jwt.decode(
                    token, configs.secret_key, algorithms=["HS256"])
            except:
                return make_response(jsonify({"message": "Invalid Token!"}), 404)

            return f(*args, **kwargs)

        return decorator

    def decode_jwt(self):
        token = request.headers.get('token')
        output = jwt.decode(token, configs.secret_key, algorithms=["HS256"])

        return output.get('username')
