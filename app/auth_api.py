from flask import Blueprint, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import re
from . import db  # Import db from app.py
# from .models import User  # Import User model for User-specific routes
from .helpers import is_valid_email, is_valid_password  # Assuming these helpers are already defined

auth_bp = Blueprint('auth_bp', __name__)

# User model (existing code for user registration and login) remains unchanged
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    user_class = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.full_name}>'

# Helper function to validate email format (already exists in your code)
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Helper function to validate password strength (already exists in your code)
def is_valid_password(password):
    # Check password length, one uppercase, one lowercase, one digit, and one special character
    password_regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(password_regex, password) is not None

# ============================
# USER REGISTRATION
# ============================
@auth_bp.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        full_name = data.get('full_name')
        phone_number = data.get('phone_number')
        age = data.get('age')
        user_class = data.get('user_class')
        email = data.get('email')
        password = data.get('password')

        # Validate all fields are present
        if not (full_name and phone_number and age and user_class and email and password):
            return jsonify({"error": "All fields are required"}), 400

        # Validate email format
        if not is_valid_email(email):
            return jsonify({"error": "Invalid email format"}), 400

        # Validate password strength
        if not is_valid_password(password):
            return jsonify({"error": "Password must meet the requirements"}), 400

        # Check if the email is already registered
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists"}), 400

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new user instance
        user = User(
            full_name=full_name,
            phone_number=phone_number,
            age=age,
            user_class=user_class,
            email=email,
            password=hashed_password
        )

        # Save to the database
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        print(f"An error occurred during registration: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# ============================
# USER LOGIN
# ============================
@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    email = data.get('email')
    password = data.get('password')

    # Validation checks
    if not (email and password):
        return jsonify({"error": "Email and Password are required"}), 400

    if not is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    try:
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            # Store user ID in session for authentication
            session['user_id'] = user.id  # Store the user ID in session

            return jsonify({
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "phone_number": user.phone_number,
                    "age": user.age,
                    "class": user.user_class,
                    "email": user.email
                }
            }), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        print(f"Login Error: {e}")
        return jsonify({"error": "An error occurred while logging in"}), 500

# ============================
# GET CURRENT USER (With Session Authentication)
# ============================
@auth_bp.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get full details of a user by their unique ID.
    """
    try:
        user = User.query.get(user_id)
        
        if user:
            return jsonify({
                "id": user.id,
                "full_name": user.full_name,
                "phone_number": user.phone_number,
                "age": user.age,
                "class": user.user_class,
                "email": user.email
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404
    
    except Exception as e:
        print(f"Fetch User Error: {e}")
        return jsonify({"error": "An error occurred while fetching the user details"}), 500