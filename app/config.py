# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'turntable.proxy.rlwy.net')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'VYQfSJYayrweYeAUZJQqaBFNPkkQmrQG')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'railway')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', '15392'))

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # To disable Flask-SQLAlchemy modification tracking
    SECRET_KEY = os.getenv('SECRET_KEY', '4d1af60b3132ae555ee9d78760d20251ed90ccbb6eba0474e124bf73e7c41196')