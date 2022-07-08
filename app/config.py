import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GCP_CRED: str = os.environ.get('GCP_CRED', 'user-api.json')
GCP_OS = os.path.join(ROOT_DIR, 'secrets', GCP_CRED)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GCP_OS
