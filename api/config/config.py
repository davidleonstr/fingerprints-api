from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    API_HOST: str = os.getenv('API_HOST')
    API_PORT: int = int(os.getenv('API_PORT'))
    API_KEY: str = os.getenv('API_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = bool(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))
    JWT_SECRET = os.getenv('JWT_SECRET')
    PASSWORD_SALT = os.getenv('PASSWORD_SALT')