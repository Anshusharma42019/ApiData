from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from dotenv import load_dotenv
from .config import Config
import os
import pymysql
import logging
from flask_migrate import Migrate

migrate = Migrate()
# Initialize MySQLdb
pymysql.install_as_MySQLdb()

# Initialize extensions
db = SQLAlchemy()
# JWTManager is no longer needed, so it's removed

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Application Factory for creating Flask app."""
    app = Flask(__name__)

    # Load configuration from Config class
    app.config.from_object(Config)

    # Database configuration
    database_url = app.config['SQLALCHEMY_DATABASE_URI']
    logger.info(f"Connecting to database: {database_url}")

    # No JWT Secret Key, since we're not using JWT anymore

    # Initialize extensions with the app instance
    db.init_app(app)
    migrate.init_app(app, db)  # Migrate without JWT
    CORS(app, origins=["*"], supports_credentials=True)

    # Register Blueprints
    from .auth_api import auth_bp
    from .content_api import content_bp
    from .admin_content_api import admin_content_bp
    from .admin_auth import admin_auth_bp
    

    # 🚀 Register without extra '/api' since it's already in the blueprint
    app.register_blueprint(auth_bp)
    app.register_blueprint(content_bp)
    app.register_blueprint(admin_content_bp)
    app.register_blueprint(admin_auth_bp)

    # Test Route
    @app.route('/')
    def home():
        return {"message": "Welcome to the API Home!"}

    # Global error handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(f"An error occurred: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    # Create database tables (only during initial app setup)
    with app.app_context():
        try:
            db.create_all()
            logger.info("Tables created successfully.")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            raise e

    return app
