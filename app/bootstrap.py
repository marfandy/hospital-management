import os
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.routes import routers

Bootstraps = Flask(__name__)
Bootstraps.register_blueprint(routers, url_prefix='/api')

CORS(Bootstraps)
