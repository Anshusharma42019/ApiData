import re
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # Import db from this module, which is initialized in __init__.py

auth_bp = Blueprint('auth_bp', __name__)
from flask_cors import CORS
CORS(auth_bp)

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

# Helper function to validate email format
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Helper function to validate password strength
def is_valid_password(password):
    # Check password length, one uppercase, one lowercase, one digit, and one special character
    password_regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(password_regex, password) is not None

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    full_name = data.get('full_name')
    phone_number = data.get('phone_number')
    age = data.get('age')
    user_class = data.get('class')
    email = data.get('email')
    password = data.get('password')

    # Validation checks
    if not (full_name and phone_number and age and user_class and email and password):
        return jsonify({"error": "All fields are required"}), 400

    # Email format validation
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    # Check if email is already in use
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    # Password strength validation
    if not is_valid_password(password):
        return jsonify({"error": "Password must be at least 8 characters long, contain at least one number, one special character, and one letter"}), 400

    hashed_password = generate_password_hash(password)

    try:
        user = User(full_name=full_name, phone_number=phone_number, age=age,
                    user_class=user_class, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        print(f"Registration Error: {e}")
        return jsonify({"error": "An error occurred while registering the user"}), 500

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

