from flask import Blueprint, jsonify
from models import Subject, Chapter, Quiz

api = Blueprint("api", __name__)

@api.route("/api/subjects", methods = ["GET"])
# @login_required
def get_subjects():
    subjects = Subject.query.all()
    return jsonify([{"id": subject.id, "name": subject.name, "description": subject.description} for subject in subjects])

@api.route("api/chapters", methods = ["GET"])
# @login_required
def get_chapters():
    chapters = Chapter.query.all()
    return jsonify([{"id": chapter.id, "name": chapter.name, "description": chapter.description} for chapter in chapters])

@api.route("api/quizzes/", methods = ["GET"])
# @login_required
def get_quizzes():
    quizzes = Quiz.query.all()
    return jsonify([{"id": quiz.id, "name": quiz.name, "description": quiz.description} for quiz in quizzes])