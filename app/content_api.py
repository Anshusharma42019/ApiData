from flask import Blueprint, jsonify, redirect, request
import os
import json
from flask import current_app as app

content_bp = Blueprint('content_bp', __name__)

# Base directory: backend/app
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
        data = get_content_file(class_number, subject, 'content')
        if not data:
            return jsonify({'error': f'{subject} content for Class {class_number} not found'}), 404
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@content_bp.route('/api/class/<int:class_number>/<subject>/quiz', methods=['GET'])
def get_quiz(class_number, subject):
    try:
        file_path = os.path.join(BASE_DIR, f'content/class_{class_number}/quiz/{subject}_quiz.json')
        print(f"Looking for file at: {file_path}")

        if not os.path.isfile(file_path):
            print("Quiz file does not exist.")
            return jsonify({'error': f'{subject} quiz for Class {class_number} not found'}), 404

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data), 200
    except Exception as e:
        print("Error in get_quiz:", e)
        return jsonify({'error': str(e)}), 500


@content_bp.route('/api/image/<class_name>/<subject>', methods=['GET'])
def get_single_image(class_name, subject):
    json_path = os.path.join(BASE_DIR, 'content/images/images.json')

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        class_key = class_name.capitalize().replace('class_', 'Class_')
        subject_key = subject.capitalize()

        class_subject_images = data.get("class_subject_images", {})
        subject_images = class_subject_images.get(class_key, {})

        image_url = subject_images.get(subject_key)
        if not image_url:
            return jsonify({"error": f"Image not found for Class {class_key} and Subject {subject_key}"}), 404

        return redirect(image_url)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🚀 NEW: Get all subjects for a specified class
@content_bp.route('/api/class/<int:class_number>/subjects', methods=['GET'])
def get_subjects(class_number):
    """
    This route fetches all subjects available for the specified class by
    scanning the folder structure inside 'content/class_<class_number>/'.
    """
    class_path = os.path.join(BASE_DIR, f'content/class_{class_number}')
    
    if not os.path.exists(class_path):
        return jsonify({"error": f"Class {class_number} not found"}), 404
    
    subjects = []
    
    for file in os.listdir(class_path):
        if file.endswith('.json') and not file.startswith('quiz'):
            subjects.append(file.replace('.json', ''))
    
    if not subjects:
        return jsonify({"error": f"No subjects found for Class {class_number}"}), 404
    
    return jsonify({"class": class_number, "subjects": subjects}), 200


