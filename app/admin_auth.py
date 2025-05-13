from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Admin
from . import db
import os

admin_auth_bp = Blueprint('admin_auth_bp', __name__)

# ================================
# ADMIN REGISTRATION (ONE-TIME ONLY)
# ================================
@admin_auth_bp.route('/api/admin/register', methods=['POST'])
def register_admin():
    data = request.json
    
    # Extract data
    username = data.get('username')
    email = data.get('email')
    password_hash = data.get('password')

    # Check if all required fields are provided
    if not (username and email and password_hash):
        return jsonify({"error": "All fields (username, email, password) are required"}), 400

    # Check if admin already exists (one admin only)
    existing_admin = Admin.query.first()
    if existing_admin:
        return jsonify({"error": "Admin already registered"}), 400

    # Hash the password before storing it
    hashed_password = generate_password_hash(password_hash)

    admin = Admin(username=username, email=email, password_hash=hashed_password)

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
    password_hash = data.get('password')

    # Check if email and password are provided
    if not (email and password_hash):
        return jsonify({"error": "Both email and password are required"}), 400

    admin = Admin.query.filter_by(email=email).first()

    if admin and check_password_hash(admin.password_hash, password_hash):
        # Store admin ID in session for authentication
        session['admin_id'] = admin.id
        
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

# ================================
# ADMIN LOGOUT
# ================================
@admin_auth_bp.route('/api/admin/logout', methods=['POST'])
def logout_admin():
    # Remove the admin ID from the session to log out
    session.pop('admin_id', None)
    
    return jsonify({"message": "Logged out successfully"}), 200
