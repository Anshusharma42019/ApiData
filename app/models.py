# models.py
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(500), nullable=False)
    uploaded_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    total_marks = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    questions = db.relationship('Question', backref='quiz', lazy=True)  # Relationship to Question model

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255))
    option_b = db.Column(db.String(255))
    option_c = db.Column(db.String(255))
    option_d = db.Column(db.String(255))
    correct_option = db.Column(db.String(5))

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    max_marks = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

class LMSContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    content_type = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

# New Admin model
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
