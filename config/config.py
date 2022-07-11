from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GCP_CRED: str = os.environ.get('GCP_CRED', 'user-api.json')
GCP_OS = os.path.join(ROOT_DIR, 'secrets', GCP_CRED)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GCP_OS


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)


class DevConfig(Config):
    DEBUG = os.environ.get('DEBUG', bool)


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    pass


config_dict = {
    'dev': DevConfig,
    'production': ProdConfig,
    'testing': TestConfig
}
