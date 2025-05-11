# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os
import pymysql
from admin_api import admin_bp

pymysql.install_as_MySQLdb()

# 🔹 Initialize the db
db = SQLAlchemy()

# 🔹 Load environment variables from .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, origins=["*"], supports_credentials=True)

    # 🔹 Configuring the app
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('Database_url')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 🔹 Initialize extensions
    db.init_app(app)

    # 🔹 Register blueprints *after* app and db are initialized
    from .auth_api import auth_bp
    from .content_api import content_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(content_bp)
    app.register_blueprint(admin_bp)
    from .admin_auth import admin_auth_bp
    app.register_blueprint(admin_auth_bp)


    # 🔹 Create tables if not exist
    with app.app_context():
        db.create_all() 

    return app
