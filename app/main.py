# app/main.py
from flask import Flask, request, jsonify
from app.content_api import content_bp
from app.auth_api import auth_bp
from app.admin_api import admin_bp
from app.admin_auth import admin_auth_bp
from app.models import db

app = Flask(__name__)
app.config.from_object('app.config.Config')
db.init_app(app)

# Register blueprints
app.register_blueprint(content_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(admin_auth_bp)

# Define Home route
@app.route('/')
def home():
    return {"message": "Welcome to the API Home!"}

# Define Test DB route
@app.route('/test-db')
def test_db():
    return {"message": "Database connection successful"}
