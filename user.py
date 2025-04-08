from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from models import Subject, Chapter, Quiz, Question, Score, db

user = Blueprint("user", __name__)

@user.route("/userhome/<int:user_id>", methods = ["GET"])
# @login_required
def user_home(user_id):
    subjects = Subject.query.all()
    return render_template("user_home.html", subjects = subjects, user_id = user_id)

@user.route("/userhome/<int:user_id>/view_chapters/<int:subject_id>", methods = ["GET"])
# @login_required
def view_chapters_user(subject_id, user_id):
    chapters = Chapter.query.filter_by(subject_id = subject_id).all()
    subject = Subject.query.get(subject_id)
    return render_template("view_chapters_user.html", chapters = chapters, subject = subject, user_id = user_id)

@user.route("/userhome/<int:user_id>/view_quiz/<int:subject_id>/<int:chapter_id>", methods = ["GET"])
# @login_required
def view_quiz_user(subject_id, chapter_id, user_id):
    quizzes = Quiz.query.filter_by(chapter_id = chapter_id).all()
    chapter = Chapter.query.get(chapter_id) 
    subject = Subject.query.get(subject_id)
    return render_template("view_quiz_user.html", quizzes = quizzes, chapter = chapter, subject = subject, user_id = user_id)

@user.route("/userhome/<int:user_id>/view_questions/<int:subject_id>/<int:chapter_id>/<int:quiz_id>", methods = ["GET", "POST"])
# @login_required
def view_questions_user(subject_id, chapter_id, quiz_id, user_id):
    questions = Question.query.filter_by(quiz_id = quiz_id).all()
    quiz = Quiz.query.get(quiz_id)
    chapter = Chapter.query.get(chapter_id)
    subject = Subject.query.get(subject_id)
    return render_template("view_questions_user.html", questions = questions, quiz = quiz, chapter = chapter, subject = subject, user_id = user_id)

@user.route('/userhome/<int:user_id>/submit_quiz/<int:quiz_id>', methods=['POST'])
# @login_required
def submit_quiz(quiz_id, user_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    score = 0
    for question in questions:
        user_answer = request.form.get(f'question_{question.id}')
        if user_answer and user_answer == question.correct_answer:
            score += 1
    new_score = Score(user_id = user_id, quiz_id=quiz_id, marks=score)
    db.session.add(new_score)
    db.session.commit()
    return redirect(url_for("user.quiz_results", quiz_id=quiz_id, user_id=user_id))

@user.route("/userhome/<int:user_id>/quiz/<int:quiz_id>/results", methods = ["GET"])
# @login_required
def quiz_results(user_id,quiz_id):
    quiz = Quiz.query.get(quiz_id)
    user_scores = Score.query.filter_by(user_id = user_id, quiz_id=quiz_id).order_by(Score.id.desc()).all()
    remaining_scores = user_scores[1:]
    latest_score = user_scores[0]
    return render_template("quiz_results.html", quiz=quiz, user_scores=user_scores, user_id=user_id, latest_score=latest_score, remaining_scores=remaining_scores)

    
