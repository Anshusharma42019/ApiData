from flask import Flask, jsonify
from .content_api import content_bp
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Accessing environment variables
SECRET_KEY = os.getenv('SECRET_KEY')
API_URL = os.getenv('API_URL')  # This will be used in your Flask routes


def create_app():
    app = Flask(__name__)
    app.register_blueprint(content_bp)

    # Home route
    @app.route('/')
    def home():
      print("Home route accessed")  # This will confirm if the home route is hit
      return jsonify({"message": "Welcome to the API Home!"})


    return app
