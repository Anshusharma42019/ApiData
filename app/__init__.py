from flask import Flask, jsonify
from .content_api import content_bp
from flask_cors import CORS  # <-- import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
API_URL = os.getenv('API_URL')


def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)  # <-- Add this line

    app.register_blueprint(content_bp)

    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to the API Home!"})

    return app
