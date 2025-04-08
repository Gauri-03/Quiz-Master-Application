from flask import Blueprint, render_template
from models import Score, User, db, Quiz, Chapter, Subject

stats = Blueprint("stats", __name__)

@stats.route("/userhome/<int:user_id>/stats")
# @login_required
def view_stats_user(user_id):
    user = User.query.get(user_id)

    user_scores = (
        Score.query.filter_by(user_id=user_id)
        .order_by(Score.id.desc()) 
        .all()
    )

    latest_scores = {}
    for score in user_scores:
        if score.quiz_id not in latest_scores:
            latest_scores[score.quiz_id] = score

    quiz_data = []
    subject_scores = {}

    subject_avg_scores = {}
    best_subject = None
    weakest_subject = None

    for quiz_id, score in latest_scores.items():
        quiz = Quiz.query.get(quiz_id)
        chapter = Chapter.query.get(quiz.chapter_id)
        subject = Subject.query.get(chapter.subject_id)

        quiz_data.append({
            "subject_name": subject.name,
            "chapter_name": chapter.name,
            "quiz_name": quiz.name,
            "latest_score": score.marks
        })

        if subject.name not in subject_scores:
            subject_scores[subject.name] = []
        subject_scores[subject.name].append(score.marks)

    if subject_scores:
        subject_avg_scores = {subject: round(sum(scores) / len(scores), 2) for subject, scores in subject_scores.items()}
        best_subject = max(subject_avg_scores, key=subject_avg_scores.get)
        weakest_subject = min(subject_avg_scores, key=subject_avg_scores.get)

    return render_template(
        "user_stats.html", 
        user=user, 
        quiz_data=quiz_data, 
        quiz_count=len(quiz_data), 
        subject_avg_scores=subject_avg_scores, 
        best_subject=best_subject, 
        weakest_subject=weakest_subject
    )

@stats.route("/adminhome/user_stats/<int:user_id>")
# @login_required
def user_info(user_id):
    user = User.query.get(user_id)

    user_scores = (
        Score.query.filter_by(user_id=user_id)
        .order_by(Score.id.desc()) 
        .all()
    )

    latest_scores = {}

    for score in user_scores:
        if score.quiz_id not in latest_scores:
            latest_scores[score.quiz_id] = score

    quiz_data = []
    subject_scores = {}

    for quiz_id, score in latest_scores.items():
        quiz = Quiz.query.get(quiz_id)
        chapter = Chapter.query.get(quiz.chapter_id)
        subject = Subject.query.get(chapter.subject_id)

        quiz_data.append({
            "subject_name": subject.name,
            "chapter_name": chapter.name,
            "quiz_name": quiz.name,
            "latest_score": score.marks
        })

        if subject.name not in subject_scores: subject_scores[subject.name] = [] 
        subject_scores[subject.name].append(score.marks)

    subject_avg_scores = {subject: round(sum(scores) / len(scores), 2) for subject, scores in subject_scores.items()}
    best_subject = max(subject_avg_scores, key=subject_avg_scores.get) if subject_avg_scores else None
    weakest_subject = min(subject_avg_scores, key=subject_avg_scores.get) if subject_avg_scores else None

    return render_template("user_info.html", user=user, quiz_data=quiz_data, quiz_count=len(quiz_data), subject_avg_scores=subject_avg_scores, best_subject=best_subject, weakest_subject=weakest_subject)

@stats.route("/adminhome/analytics")
# @login_required
def admin_analytics():
    users = User.query.all()  
    total_users = len(users)  

    user_avg_scores = {}

    for user in users:
        user_scores = (
            Score.query.filter_by(user_id=user.id)
            .order_by(Score.id.desc())
            .all()
        )

        latest_scores = {}

        for score in user_scores:
            if score.quiz_id not in latest_scores:
                latest_scores[score.quiz_id] = score  

        if latest_scores:  
            avg_score = round(
                sum(score.marks for score in latest_scores.values()) / len(latest_scores), 2
            )
            user_avg_scores[user.username] = avg_score

    best_user = max(user_avg_scores, key=user_avg_scores.get) if user_avg_scores else None
    worst_user = min(user_avg_scores, key=user_avg_scores.get) if user_avg_scores else None

    subject_attempts = {}
    all_scores = Score.query.all()

    for score in all_scores:
        quiz = Quiz.query.get(score.quiz_id)
        chapter = Chapter.query.get(quiz.chapter_id)
        subject = Subject.query.get(chapter.subject_id)

        subject_attempts[subject.name] = subject_attempts.get(subject.name, 0) + 1

    most_popular_subject = (
        max(subject_attempts, key=subject_attempts.get) if subject_attempts else None)

    return render_template("admin_analytics.html",total_users=total_users,best_user=best_user,worst_user=worst_user,most_popular_subject=most_popular_subject,user_avg_scores=user_avg_scores)

