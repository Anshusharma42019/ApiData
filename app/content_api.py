from flask import Blueprint, jsonify, redirect, request, Response
import requests
import os
import json
import re
from . import db  # Importing db for MySQL connection
from .models import Video, Quiz, LMSContent  # Importing models for MySQL interaction
# Load image data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_JSON_PATH = os.path.join(BASE_DIR, 'content/images/images.json')

try:
    with open(IMAGE_JSON_PATH, 'r', encoding='utf-8') as f:
        image_data = json.load(f)
except Exception as e:
    print(f"Error loading image data: {e}")
    image_data = {}

content_bp = Blueprint('content_bp', __name__)

# Base directory for JSON files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Helper function to get the content file
def get_content_file(class_number, subject, file_type):
    try:
        if file_type == 'quiz':
            file_path = os.path.join(BASE_DIR, f'content/class_{class_number}/quiz/{subject}_quiz.json')
        else:
            file_path = os.path.join(BASE_DIR, f'content/class_{class_number}/{subject}.json')

        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File for {subject} not found.")

        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        return None
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return None


# Dynamic route for fetching content for any class and subject from JSON files

@content_bp.route('/api/image/class_<class_name>/<subject>', methods=['GET'])
def get_images(class_name, subject):
    # Normalize keys to match your JSON structure
    key_class = f"Class_{class_name}"   # e.g., '3' => 'Class_3'
    key_subject = subject.capitalize()  # e.g., 'english' => 'English'

    images_dict = image_data.get('class_subject_images', {})

    if key_class not in images_dict:
        return jsonify({'error': f'Class {key_class} not found'}), 404

    if key_subject not in images_dict[key_class]:
        return jsonify({'error': f'Images for {key_subject} in {key_class} not found'}), 404

    image_url = images_dict[key_class][key_subject]

    try:
        resp = requests.get(image_url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch image from URL: {image_url} - Error: {e}")
        return jsonify({'error': 'Failed to fetch image from source URL'}), 502

    content_type = resp.headers.get('Content-Type', 'image/jpeg')

    return Response(resp.content, content_type=content_type)

@content_bp.route('/api/class/<int:class_number>/<subject>/content', methods=['GET'])
def get_content(class_number, subject):
    data = get_content_file(class_number, subject, 'content')
    if not data:
        return jsonify({'error': f'{subject} content for Class {class_number} not found'}), 404
    return jsonify(data), 200


# Fetch Quiz data for a specific class and subject from JSON files
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


# 🚀 NEW: Add Video to MySQL
@content_bp.route('/api/admin/add-video', methods=['POST'])
def add_video():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    title = data.get('title')
    description = data.get('description')
    video_url = data.get('video_url')

    # Validation
    if not (title and description and video_url):
        return jsonify({"error": "All fields are required"}), 400

    try:
        # Insert video into the MySQL database
        video = Video(title=title, description=description, video_url=video_url)
        db.session.add(video)
        db.session.commit()
        return jsonify({"message": "Video added successfully"}), 201
    except Exception as e:
        print(f"Add Video Error: {e}")
        return jsonify({"error": "An error occurred while adding the video"}), 500


# 🚀 NEW: Add Quiz to MySQL
@content_bp.route('/api/admin/add-quiz', methods=['POST'])
def add_quiz():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    title = data.get('title')
    description = data.get('description')
    total_marks = data.get('total_marks')

    # Validation
    if not (title and description and total_marks):
        return jsonify({"error": "All fields are required"}), 400

    try:
        # Insert quiz into the MySQL database
        quiz = Quiz(title=title, description=description, total_marks=total_marks)
        db.session.add(quiz)
        db.session.commit()
        return jsonify({"message": "Quiz added successfully"}), 201
    except Exception as e:
        print(f"Add Quiz Error: {e}")
        return jsonify({"error": "An error occurred while adding the quiz"}), 500


# 🚀 NEW: Add LMS Content to MySQL
@content_bp.route('/api/admin/add-lms-content', methods=['POST'])
def add_lms_content():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    title = data.get('title')
    content = data.get('content')
    content_type = data.get('content_type')

    # Validation
    if not (title and content and content_type):
        return jsonify({"error": "All fields are required"}), 400

    try:
        # Insert LMS content into the MySQL database
        lms_content = LMSContent(title=title, content=content, content_type=content_type)
        db.session.add(lms_content)
        db.session.commit()
        return jsonify({"message": "LMS Content added successfully"}), 201
    except Exception as e:
        print(f"Add LMS Content Error: {e}")
        return jsonify({"error": "An error occurred while adding the LMS content"}), 500


# 🚀 NEW: Get all Videos from MySQL
@content_bp.route('/api/videos', methods=['GET'])
def get_videos():
    try:
        videos = Video.query.all()
        video_list = [
            {
                "id": video.id,
                "title": video.title,
                "description": video.description,
                "video_url": video.video_url,
                "uploaded_at": video.uploaded_at
            } for video in videos
        ]
        return jsonify(video_list), 200
    except Exception as e:
        print(f"Fetch Videos Error: {e}")
        return jsonify({"error": "An error occurred while fetching the videos"}), 500


# 🚀 NEW: Get all Quizzes from MySQL
@content_bp.route('/api/quizzes', methods=['GET'])
def get_quizzes():
    try:
        quizzes = Quiz.query.all()
        quiz_list = [
            {
                "id": quiz.id,
                "title": quiz.title,
                "description": quiz.description,
                "total_marks": quiz.total_marks,
                "created_at": quiz.created_at
            } for quiz in quizzes
        ]
        return jsonify(quiz_list), 200
    except Exception as e:
        print(f"Fetch Quizzes Error: {e}")
        return jsonify({"error": "An error occurred while fetching the quizzes"}), 500


# 🚀 NEW: Get all LMS Content from MySQL
@content_bp.route('/api/lms-content', methods=['GET'])
def get_lms_content():
    try:
        lms_content_list = LMSContent.query.all()
        lms_content = [
            {
                "id": content.id,
                "title": content.title,
                "content": content.content,
                "content_type": content.content_type,
                "created_at": content.created_at
            } for content in lms_content_list
        ]
        return jsonify(lms_content), 200
    except Exception as e:
        print(f"Fetch LMS Content Error: {e}")
        return jsonify({"error": "An error occurred while fetching the LMS content"}), 500


# 🚀 NEW: Get all subjects for a specified class
@content_bp.route('/api/class/<int:class_number>/subjects', methods=['GET'])
def get_subjects(class_number):
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

@content_bp.route('/api/content/test', methods=['GET'])
def test_content():
    from . import db  # ✅ Import inside the function
    return {"message": "Content API working!"}
