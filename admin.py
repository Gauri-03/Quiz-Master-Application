from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Subject, User, db, Chapter, Quiz, Question

admin = Blueprint("admin", __name__)

@admin.route("/adminhome", methods = ["GET"])
# @login_required
def admin_home():
    subjects = Subject.query.all()
    return render_template("admin_home.html", subjects = subjects)

@admin.route("/adminhome/create_subject", methods = ["GET","POST"])
# @login_required
def create_subject():
    if request.method == "POST":
        new_subject_name = request.form.get("name")
        new_subject_description = request.form.get("description")
        if Subject.query.filter_by(name = new_subject_name).first():
            flash("Subject already exists!", category = 'error')
            return redirect(url_for("admin.admin_home"))
        else:
            new_subject = Subject(name = new_subject_name, description = new_subject_description)
            db.session.add(new_subject)
            db.session.commit()
            flash("Subject added successfully!", category= "success")
            return redirect(url_for("admin.admin_home"))
    else:
        return redirect(url_for("admin.admin_home"))

@admin.route("/adminhome/update_subject/<int:subject_id>", methods = ["GET","POST"])
# @login_required
def update_subject(subject_id):
    subject = Subject.query.filter_by(id = subject_id).first()
    if request.method == "POST":
        updated_name = request.form.get("name")
        updated_description = request.form.get("description")
        
        if updated_name != subject.name:
            if not updated_name:
                flash("Name required!", category= "error")
                return redirect(url_for("admin.admin_home"))
            
            if Subject.query.filter_by(name = updated_name).first():
                flash("Subject already exists!", category= "error")
                return redirect(url_for("admin.admin_home"))
            
            subject.name = updated_name
            db.session.commit()
            flash("Subject name updated successfully!", category= "success")
        
        if updated_description != subject.description:
            subject.description = updated_description
            db.session.commit()
            flash("Subject description updated successfully!", category = "success")
    
    # Fetch all subjects to pass to the template
    subjects = Subject.query.all()
    return render_template("admin_home.html", subjects=subjects)

@admin.route("/adminhome/delete_subject/<int:subject_id>", methods=["POST"])
# @login_required
def delete_subject(subject_id):
    if request.method == "POST":
        chapters = Chapter.query.filter_by(subject_id = subject_id)
        for chapter in chapters:
            quizzes = Quiz.query.filter_by(chapter_id = chapter.id)
            for quiz in quizzes:
                questions = Question.query.filter_by(quiz_id = quiz.id)
                for question in questions:
                    db.session.delete(question)
                    db.session.commit()
                db.session.delete(quiz)
                db.session.commit()
            db.session.delete(chapter)
            db.session.commit()
        subject = Subject.query.get(subject_id)
        db.session.delete(subject)
        db.session.commit()
        flash("Subject deleted successfully!", category="success")
    return redirect(url_for("admin.admin_home"))

    
@admin.route("/adminhome/view_chapters/<int:subject_id>", methods = ["GET"])
# @login_required
def view_chapters(subject_id):
    chapters = Chapter.query.filter_by(subject_id = subject_id)
    subject = Subject.query.get(subject_id)
    return render_template("view_chapters.html", chapters = chapters, subject= subject)

@admin.route("/adminhome/create_chapter/<int:subject_id>", methods = ["GET", "POST"])
# @login_required
def create_chapter(subject_id):
    if request.method == "POST":
        new_chapter_name = request.form.get("name")
        new_chapter_description = request.form.get("description")
        if Chapter.query.filter_by(name = new_chapter_name).first():
            flash("Chapter already exists!", category = "error")
            return redirect(url_for("admin.view_chapters", subject_id = subject_id))
        else:
            new_chapter = Chapter(name = new_chapter_name, description = new_chapter_description, subject_id = subject_id)
            db.session.add(new_chapter)
            db.session.commit()
            flash("Chapter added successfully!", category = "success")
            return redirect(url_for("admin.view_chapters", subject_id = subject_id))
    return render_template("create_chapter.html", subject_id = subject_id)

@admin.route("/adminhome/update_chapter/<int:subject_id>/<int:chapter_id>", methods=["GET", "POST"])
def update_chapter(subject_id, chapter_id):
    chapter = Chapter.query.filter_by(id=chapter_id, subject_id=subject_id).first()
    subject = Subject.query.get(subject_id)

    if not chapter:
        flash("Chapter not found!", category="error")
        return redirect(url_for("admin.view_chapters", subject_id=subject_id))

    if request.method == "POST":
        updated_name = request.form.get("name")
        updated_description = request.form.get("description")

        if updated_name and updated_name != chapter.name:
            existing_chapter = Chapter.query.filter_by(name=updated_name, subject_id=subject_id).first()
            if existing_chapter:
                flash("Chapter with this name already exists in this subject!", category="error")
            else:
                chapter.name = updated_name
                db.session.commit()
                flash("Chapter name updated successfully!", category="success")

        if updated_description and updated_description != chapter.description:
            chapter.description = updated_description
            db.session.commit()
            flash("Chapter description updated successfully!", category="success")

    chapters = Chapter.query.filter_by(subject_id=subject_id).all()

    return render_template("view_chapters.html", chapters=chapters, subject=subject)


@admin.route("/adminhome/delete_chapter/<int:subject_id>/<int:chapter_id>", methods=["POST"])
# @login_required
def delete_chapter(subject_id, chapter_id):
    if request.method == "POST":
        quizzes = Quiz.query.filter_by(chapter_id = chapter_id)
        for quiz in quizzes:
            questions = Question.query.filter_by(quiz_id = quiz.id)
            for question in questions:
                db.session.delete(question)
                db.session.commit()
            db.session.delete(quiz)
            db.session.commit()
        chapter = Chapter.query.get(chapter_id)
        db.session.delete(chapter)
        db.session.commit()
        flash("Chapter deleted successfully!", category="success")
    return redirect(url_for("admin.view_chapters", subject_id=subject_id))

@admin.route("/adminhome/view_quiz/<int:subject_id>/<int:chapter_id>", methods = ["GET", "POST"])
# @login_required
def view_quiz(subject_id, chapter_id):
    quizzes = Quiz.query.filter_by(chapter_id = chapter_id)
    chapter = Chapter.query.get(chapter_id)
    subject = Subject.query.get(subject_id)
    return render_template("view_quiz.html", chapter = chapter, subject = subject, quizzes = quizzes)

@admin.route("/adminhome/create_quiz/<int:subject_id>/<int:chapter_id>", methods = ["GET", "POST"])
# @login_required
def create_quiz(subject_id, chapter_id):
    if request.method == "POST":
        new_quiz_name = request.form.get("name")
        new_quiz_description = request.form.get("description")
        if Quiz.query.filter_by(name = new_quiz_name).first():
            flash("Quiz already exists!", category = "error")
            return redirect(url_for("admin.view_quiz", subject_id = subject_id, chapter_id = chapter_id))
        else:
            new_quiz = Quiz(name = new_quiz_name, description = new_quiz_description, chapter_id = chapter_id)
            db.session.add(new_quiz)
            db.session.commit()
            flash("Quiz added successfully!", category = "success")
            return redirect(url_for("admin.view_quiz", subject_id = subject_id, chapter_id = chapter_id))
    return render_template("view_quiz.html", subject_id = subject_id, chapter_id = chapter_id)

@admin.route("/adminhome/update_quiz/<int:subject_id>/<int:chapter_id>/<int:quiz_id>", methods = ["GET", "POST"])
# @login_required
def update_quiz(subject_id, chapter_id, quiz_id):
    quiz = Quiz.query.filter_by(id = quiz_id).first()
    chapter = Chapter.query.get(chapter_id)
    subject = Subject.query.get(subject_id)
    if request.method == "POST":
        updated_name = request.form.get("name")
        updated_description = request.form.get("description")
        if updated_name != quiz.name:
            if not updated_name:
                flash("Name required!", category= "error")
                return redirect(url_for("admin.update_quiz", subject_id = subject_id, chapter_id = chapter_id, quiz_id = quiz_id))
            if Quiz.query.filter_by(name = updated_name).first():
                flash("Quiz already exists!", category= "error")
                return redirect(url_for("admin.update_quiz", subject_id = subject_id, chapter_id = chapter_id, quiz_id = quiz_id))
            quiz.name = updated_name
            db.session.commit()
            flash("Quiz name updated successfully!", category= "success")
        if updated_description != quiz.description:
            quiz.description = updated_description
            db.session.commit()
            flash("Quiz description updated successfully!", category = "success")
        quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
        
    return render_template("view_quiz.html", subject = subject, chapter = chapter, quiz = quiz, quizzes = quizzes)

@admin.route("/adminhome/delete_quiz/<int:subject_id>/<int:chapter_id>/<int:quiz_id>", methods=["POST"])
# @login_required
def delete_quiz(subject_id, chapter_id, quiz_id):
    if request.method == "POST":
        questions = Question.query.filter_by(quiz_id = quiz_id)
        for question in questions:
            db.session.delete(question)
            db.session.commit()
        quiz = Quiz.query.get(quiz_id)
        db.session.delete(quiz)
        db.session.commit()
        flash("Quiz deleted successfully!", category="success")
    return redirect(url_for("admin.view_quiz", subject_id=subject_id, chapter_id=chapter_id))

@admin.route("/adminhome/attempt_quiz/<int:subject_id>/<int:chapter_id>/<int:quiz_id>", methods = ["GET", "POST"])
# @login_required
def view_questions(subject_id, chapter_id, quiz_id):
    questions = Question.query.filter_by(quiz_id = quiz_id)
    quiz = Quiz.query.get(quiz_id)
    chapter = Chapter.query.get(chapter_id)
    subject = Subject.query.get(subject_id)
    return render_template("attempt_quiz.html", quiz = quiz, chapter = chapter, subject = subject, questions = questions)

@admin.route("/adminhome/create_question/<int:subject_id>/<int:chapter_id>/<int:quiz_id>", methods = ["GET", "POST"])
# @login_required
def create_question(subject_id, chapter_id, quiz_id):
    if request.method == "POST":
        quiz = Quiz.query.get(quiz_id)
        chapter = Chapter.query.get(chapter_id)
        subject = Subject.query.get(subject_id)
        statement = request.form.get("statement")
        option_a = request.form.get("optiona")
        option_b = request.form.get("optionb")
        option_c = request.form.get("optionc")
        option_d = request.form.get("optiond")
        correct_answer = request.form.get("correct_answer")
        
        all_options = [option_a, option_b, option_c, option_d]
        
        if Question.query.filter_by(statement=statement).first():
            flash("Question already exists!", category="error")
            return redirect(url_for("admin.view_questions", subject_id=subject_id, chapter_id=chapter_id, quiz_id=quiz_id))
        
        if correct_answer not in all_options:
            flash("Correct answer must be one of the provided options!", category="error")
            return redirect(url_for("admin.view_questions", subject_id=subject_id, chapter_id=chapter_id, quiz_id=quiz_id))
        
        new_question = Question(statement=statement, option_a=option_a, option_b=option_b, option_c=option_c, option_d=option_d, correct_answer=correct_answer, quiz_id=quiz_id)
        db.session.add(new_question)
        db.session.commit()
        flash("Question added successfully!", category="success")
        return redirect(url_for("admin.view_questions", subject_id=subject_id, chapter_id=chapter_id, quiz_id=quiz_id))
    
    return render_template("attempt_quiz.html", subject=subject, chapter=chapter, quiz=quiz)

@admin.route("/adminhome/update_question/<int:subject_id>/<int:chapter_id>/<int:quiz_id>/<int:question_id>", methods = ["GET", "POST"])
# @login_required
def update_question(subject_id, chapter_id, quiz_id,question_id):
    question = Question.query.filter_by(id = question_id).first()
    quiz = Quiz.query.get(quiz_id)
    chapter = Chapter.query.get(chapter_id)
    subject = Subject.query.get(subject_id)
    if request.method == "POST":
        updated_statement = request.form.get("statement")
        updated_option_a = request.form.get("optiona")
        updated_option_b = request.form.get("optionb")
        updated_option_c = request.form.get("optionc")
        updated_option_d = request.form.get("optiond")
        all_options = [updated_option_a, updated_option_b, updated_option_c, updated_option_d]
        updated_correct_answer = request.form.get("correct_answer")
        
        if updated_statement != question.statement:
            if not updated_statement:
                flash("Statement required!", category = "error")
                return redirect(url_for("admin.update_question", subject_id = subject_id, chapter_id = chapter_id, quiz_id = quiz_id, question_id = question_id))
            if Question.query.filter_by(statement = updated_statement).first():
                flash("Question already exists!", category = "error")
                return redirect(url_for("admin.update_question", subject_id = subject_id, chapter_id = chapter_id, quiz_id = quiz_id, question_id = question_id))
            question.statement = updated_statement
            db.session.commit()
            flash("Question statement updated successfully!", category = "success")
        if updated_correct_answer not in all_options:
            flash("Correct answer must be one of the provided options!", category="error")
            return redirect(url_for("admin.update_question", subject_id=subject_id, chapter_id=chapter_id, quiz_id=quiz_id, question_id=question_id))
        if updated_option_a != question.option_a:
            question.option_a = updated_option_a
            db.session.commit()
            flash("Option A updated successfully!", category = "success")
        if updated_option_b != question.option_b:
            question.option_b = updated_option_b
            db.session.commit()
            flash("Option B updated successfully!", category = "success")
        if updated_option_c != question.option_c:
            question.option_c = updated_option_c
            db.session.commit()
            flash("Option C updated successfully!", category = "success")
        if updated_option_d != question.option_d:
            question.option_d = updated_option_d
            db.session.commit()
            flash("Option D updated successfully!", category = "success")
        if updated_correct_answer != question.correct_answer:
            question.correct_answer = updated_correct_answer
            db.session.commit()
            flash("Correct answer updated successfully!", category = "success")
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return render_template("attempt_quiz.html", subject = subject, chapter = chapter, quiz = quiz, question = question, questions = questions)

@admin.route("/adminhome/delete_question/<int:subject_id>/<int:chapter_id>/<int:quiz_id>/<int:question_id>", methods=["POST"])
# @login_required
def delete_question(subject_id, chapter_id, quiz_id, question_id):
    if request.method == "POST":
        question = Question.query.get(question_id)
        if question:
            db.session.delete(question)
            db.session.commit()
            flash("Question deleted successfully!", category="success")
        else:
            flash("Question not found!", category="error")
    return redirect(url_for("admin.view_questions", subject_id=subject_id, chapter_id=chapter_id, quiz_id=quiz_id))

@admin.route("/adminhome/search", methods=["GET", "POST"])
# @login_required
def search():
    if request.method == "POST":
        search_term = request.form.get("search")
        search_type = request.form.get("search_type")
        
        if search_type == "user":
            users = User.query.filter(User.username.ilike(f"%{search_term}%")).all()
            if not users:
                flash(f"No users found matching '{search_term}'", category="error")
                return render_template("search_admin.html")
            return render_template("view_users.html", users=users, search_term=search_term)

        elif search_type == "subject":
            subjects = Subject.query.filter(Subject.name.ilike(f"%{search_term}%")).all()
            if not subjects:
                flash(f"No subjects found matching '{search_term}'", category="error")
                return render_template("search_admin.html")
            return render_template("admin_home.html", subjects=subjects, search_term=search_term)

    return render_template("search_admin.html")

@admin.route("/adminhome/view_users", methods=["GET", "POST"])
# @login_required
def view_users():
    users = User.query.all()
    return render_template("view_users.html", users=users)

@admin.route("/adminhome/delete_user/<int:user_id>", methods=["POST"])
# @login_required
def delete_user(user_id):
    if request.method == "POST":
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            flash("User deleted successfully!", category="success")
        else:
            flash("User not found!", category="error")
    return redirect(url_for("admin.view_users"))