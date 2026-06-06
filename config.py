import os
from pathlib import Path

class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY")
    # # Uploading DataBase
    # BASE_DIR = Path(__file__).resolve().parent
    # UPLOAD_DIR = BASE_DIR / "static" / "uploads"
    # UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # اگر نبود، بساز

    # DataBase Config
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "airplane.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = True
    pass

class DevelopmentConfig(Config):
    pass