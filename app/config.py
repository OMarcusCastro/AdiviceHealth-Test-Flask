import os

from dotenv import load_dotenv
load_dotenv()

print("oiii", os.getenv('DATABASE_URL'))


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://carford_user:password@db:5432/carford_db')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///carford.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
