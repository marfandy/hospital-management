import os
from pydantic import BaseSettings, Field


class Configs(BaseSettings):
    root_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gcp_cred: str = Field("user-api.json", env="gcp_cred")


configs = Configs()

gcp_os = os.path.join(configs.root_dir, "secrets", configs.gcp_cred)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_os
