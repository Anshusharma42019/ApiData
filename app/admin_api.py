# admin_api.py
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from .models import Admin
from . import db
import jwt
import datetime
from functools import wraps
from flask import current_app as app

admin_bp = Blueprint('admin_bp', __name__)

# Secret key for JWT
SECRET_KEY = "your_secret_key"

# JWT Token Required Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing!"}), 403
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_admin = Admin.query.filter_by(id=data['id']).first()
        except:
            return jsonify({"error": "Token is invalid!"}), 403
        return f(current_admin, *args, **kwargs)
    return decorated

# Admin Registration
@admin_bp.route('/api/admin/register', methods=['POST'])
def register_admin():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not (username and email and password):
        return jsonify({"error": "All fields are required"}), 400

    if Admin.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_admin = Admin(username=username, email=email, password=hashed_password)
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({"message": "Admin registered successfully"}), 201

# Admin Login
@admin_bp.route('/api/admin/login', methods=['POST'])
def login_admin():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not (email and password):
        return jsonify({"error": "Email and Password are required"}), 400

    admin = Admin.query.filter_by(email=email).first()

    if admin and admin.check_password(password):
        token = jwt.encode({
            'id': admin.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, SECRET_KEY, algorithm="HS256")
        
        return jsonify({
            "message": "Login successful",
            "token": token
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
