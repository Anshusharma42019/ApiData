# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from .config import Config
import os
import pymysql

pymysql.install_as_MySQLdb()

# Initialize the db
db = SQLAlchemy()
# migrate = Migrate()

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["*"], supports_credentials=True)

# Database configuration
database_url = f"mysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DATABASE}"
print(f"Connecting to database: {database_url}")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
# migrate.init_app(app, db)

# Register blueprints
from .auth_api import auth_bp
from .content_api import content_bp
from .admin_api import admin_bp
from .admin_auth import admin_auth_bp

app.register_blueprint(auth_bp)
app.register_blueprint(content_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(admin_auth_bp)

# Test Route
@app.route('/')
def home():
    return {"message": "Welcome to the API Home!"}

# Create database tables if not exist
with app.app_context():
    try:
        db.create_all()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
