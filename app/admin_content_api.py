from flask import Blueprint, jsonify, request, session
from .models import Video, Quiz, Question, Test, LMSContent, Admin
from . import db
from functools import wraps

admin_content_bp = Blueprint('admin_content_bp', __name__)

# ==============================
# Middleware to Verify Admin
# ==============================
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin_id = session.get('admin_id')
        if not admin_id:
            return jsonify({"error": "Admin access required"}), 403

        admin = Admin.query.get(admin_id)
        if not admin:
            return jsonify({"error": "Invalid admin session"}), 403
        
        return f(*args, **kwargs)
    return decorated_function

# ==============================
# Video CRUD Operations
# ==============================
@admin_content_bp.route('/api/admin/videos', methods=['POST'])
@admin_required
def create_video():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    video_url = data.get('video_url')

    if not (title and video_url):
        return jsonify({"error": "Title and Video URL are required"}), 400

    new_video = Video(title=title, description=description, video_url=video_url)
    db.session.add(new_video)
    db.session.commit()
    return jsonify({"message": "Video created successfully"}), 201


@admin_content_bp.route('/api/admin/videos', methods=['GET'])
@admin_required
def get_all_videos():
    videos = Video.query.all()
    return jsonify([{
        "id": v.id,
        "title": v.title,
        "description": v.description,
        "video_url": v.video_url
    } for v in videos]), 200


@admin_content_bp.route('/api/admin/videos/<int:video_id>', methods=['DELETE'])
@admin_required
def delete_video(video_id):
    video = Video.query.get(video_id)
    if not video:
        return jsonify({"error": "Video not found"}), 404

    db.session.delete(video)
    db.session.commit()
    return jsonify({"message": "Video deleted successfully"}), 200

# ==============================
# Quiz and Questions CRUD Operations
# ==============================
@admin_content_bp.route('/api/admin/quizzes', methods=['POST'])
@admin_required
def create_quiz():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    total_marks = data.get('total_marks')
    questions = data.get('questions', [])

    if not (title and total_marks):
        return jsonify({"error": "Title and Total Marks are required"}), 400

    new_quiz = Quiz(title=title, description=description, total_marks=total_marks)
    db.session.add(new_quiz)
    db.session.commit()

    for question in questions:
        new_question = Question(
            quiz_id=new_quiz.id,
            question_text=question.get('question_text'),
            option_a=question.get('option_a'),
            option_b=question.get('option_b'),
            option_c=question.get('option_c'),
            option_d=question.get('option_d'),
            correct_option=question.get('correct_option')
        )
        db.session.add(new_question)

    db.session.commit()
    return jsonify({"message": "Quiz and Questions created successfully"}), 201


@admin_content_bp.route('/api/admin/quizzes', methods=['GET'])
@admin_required
def get_all_quizzes():
    quizzes = Quiz.query.all()
    return jsonify([{
        "id": q.id,
        "title": q.title,
        "description": q.description,
        "total_marks": q.total_marks,
        "questions": [{
            "id": qs.id,
            "question_text": qs.question_text,
            "option_a": qs.option_a,
            "option_b": qs.option_b,
            "option_c": qs.option_c,
            "option_d": qs.option_d,
            "correct_option": qs.correct_option
        } for qs in q.questions]
    } for q in quizzes]), 200


@admin_content_bp.route('/api/admin/quizzes/<int:quiz_id>', methods=['DELETE'])
@admin_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    db.session.delete(quiz)
    db.session.commit()
    return jsonify({"message": "Quiz deleted successfully"}), 200

# ==============================
# Test CRUD Operations
# ==============================
@admin_content_bp.route('/api/admin/tests', methods=['POST'])
@admin_required
def create_test():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    max_marks = data.get('max_marks')

    if not (title and max_marks):
        return jsonify({"error": "Title and Max Marks are required"}), 400

    new_test = Test(title=title, description=description, max_marks=max_marks)
    db.session.add(new_test)
    db.session.commit()
    return jsonify({"message": "Test created successfully"}), 201


@admin_content_bp.route('/api/admin/tests', methods=['GET'])
@admin_required
def get_all_tests():
    tests = Test.query.all()
    return jsonify([{
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "max_marks": t.max_marks
    } for t in tests]), 200


@admin_content_bp.route('/api/admin/tests/<int:test_id>', methods=['DELETE'])
@admin_required
def delete_test(test_id):
    test = Test.query.get(test_id)
    if not test:
        return jsonify({"error": "Test not found"}), 404

    db.session.delete(test)
    db.session.commit()
    return jsonify({"message": "Test deleted successfully"}), 200

# ==============================
# LMS Content CRUD Operations
# ==============================
@admin_content_bp.route('/api/admin/lms-content', methods=['POST'])
@admin_required
def create_lms_content():
    data = request.json
    title = data.get('title')
    content = data.get('content')
    content_type = data.get('content_type')

    if not (title and content and content_type):
        return jsonify({"error": "All fields are required"}), 400

    new_content = LMSContent(title=title, content=content, content_type=content_type)
    db.session.add(new_content)
    db.session.commit()
    return jsonify({"message": "LMS Content created successfully"}), 201


@admin_content_bp.route('/api/admin/lms-content', methods=['GET'])
@admin_required
def get_all_lms_content():
    contents = LMSContent.query.all()
    return jsonify([{
        "id": c.id,
        "title": c.title,
        "content": c.content,
        "content_type": c.content_type
    } for c in contents]), 200


@admin_content_bp.route('/api/admin/lms-content/<int:content_id>', methods=['DELETE'])
@admin_required
def delete_lms_content(content_id):
    content = LMSContent.query.get(content_id)
    if not content:
        return jsonify({"error": "Content not found"}), 404

    db.session.delete(content)
    db.session.commit()
    return jsonify({"message": "LMS Content deleted successfully"}), 200
