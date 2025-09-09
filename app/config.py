import os
from dotenv import load_dotenv
load_dotenv()

def require_env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return v

MONGO_URI = require_env("MONGO_URI")           
SECRET_KEY = require_env("SECRET_KEY")         

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
DB_NAME = os.getenv("DB_NAME", "RecruitmentSystem")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
ALLOW_INVALID_CERTS = os.getenv("ALLOW_INVALID_CERTS", "false").lower() == "true"
