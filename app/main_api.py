# app/main_api.py
from flask import Blueprint

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def home():
    return {"message": "Welcome to the API Home!"}
