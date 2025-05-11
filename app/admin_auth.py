# app/admin_auth.py
from flask import Blueprint, request, jsonify
from .models import Admin
from . import db

admin_auth_bp = Blueprint('admin_auth_bp', __name__)

# ================================
# ADMIN REGISTRATION
# ================================
@admin_auth_bp.route('/api/admin/register', methods=['POST'])
def register_admin():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not (username and email and password):
        return jsonify({"error": "All fields are required"}), 400

    # Check if admin already exists
    if Admin.query.filter_by(email=email).first():
        return jsonify({"error": "Admin already exists"}), 400

    admin = Admin(username=username, email=email)
    admin.set_password(password)
    
    try:
        db.session.add(admin)
        db.session.commit()
        return jsonify({"message": "Admin registered successfully"}), 201
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred during registration"}), 500

# ================================
# ADMIN LOGIN
# ================================
@admin_auth_bp.route('/api/admin/login', methods=['POST'])
def login_admin():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    admin = Admin.query.filter_by(email=email).first()

    if admin and admin.check_password(password):
        return jsonify({
            "message": "Login successful",
            "admin": {
                "id": admin.id,
                "username": admin.username,
                "email": admin.email
            }
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
