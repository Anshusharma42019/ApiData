from flask import Blueprint, jsonify
import os
import json

content_bp = Blueprint('content_bp', __name__)


# Base directory: backend/app
# NEW — points directly to /backend/app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
@content_bp.route('/')
def home():
    return jsonify({"message": "Welcome from Blueprint!"})



# Helper function to get the content file
def get_content_file(class_number, subject, file_type):
    try:
        if file_type == 'quiz':
            file_path = os.path.join(BASE_DIR, f'content/class_{class_number}/quiz/{subject}_quiz.json')
        else:
            file_path = os.path.join(BASE_DIR, f'content/class_{class_number}/{subject}.json')

        print("Looking for file at:", file_path)

        if not os.path.isfile(file_path):
            print("File does not exist.")
            return None

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return data

    except Exception as e:
        print("Error reading file:", e)
        return None


# Dynamic route for fetching content for any class and subject
@content_bp.route('/api/class/<int:class_number>/<subject>/content', methods=['GET'])
def get_content(class_number, subject):
    try:
        data = get_content_file(class_number, subject, 'content')  # 'content' refers to the content file
        if not data:
            return jsonify({'error': f'{subject} content for Class {class_number} not found'}), 404
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/api/class/<int:class_number>/<subject>/quiz', methods=['GET'])
def get_quiz(class_number, subject):
    try:
        # Safely build file path
        file_path = os.path.join(BASE_DIR, f'content/class_{class_number}/quiz/{subject}_quiz.json')
        print(f"Looking for file at: {file_path}")  # Debugging line

        if not os.path.isfile(file_path):
            print("Quiz file does not exist.")
            return jsonify({'error': f'{subject} quiz for Class {class_number} not found'}), 404

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data), 200
    except Exception as e:
        print("Error in get_quiz:", e)
        return jsonify({'error': str(e)}), 500


@content_bp.route('/test-read', methods=['GET'])
def test_read():
    test_path = os.path.join(BASE_DIR, 'content/class_1/quiz/english_quiz.json')
    try:
        with open(test_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e), "path": test_path})

@content_bp.route('/api/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Test route works!"}), 200

@content_bp.route('/api/images/<class_name>', methods=['GET'])
def get_class_subject_images(class_name):
    # Construct path
    json_path = os.path.join(os.path.dirname(__file__), '../content/images/images.json')

    # Load the JSON
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        class_subject_images = data.get("class_subject_images", {})
        result = class_subject_images.get(class_name)

        if result:
            return jsonify({"class": class_name, "subjects": result}), 200
        else:
            return jsonify({"error": "Class not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500