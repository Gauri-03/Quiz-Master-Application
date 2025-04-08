from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "quizmaster.db"

class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password 

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.Text, unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    qualification = db.Column(db.Text, nullable = False)
    dob = db.Column(db.Date)
    score= db.relationship('Score', backref = 'user')

class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text, nullable = False)
    description = db.Column(db.Text)
    chapters = db.relationship('Chapter', backref = 'subject')

class Chapter(db.Model):
    __tablename__ = "chapter"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text, nullable = False)
    description = db.Column(db.Text)
    quiz = db.relationship('Quiz', backref = 'chapter')
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    
class Quiz(db.Model):
    __tablename__ = "quiz"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text, nullable = False)
    description = db.Column(db.Text)
    question = db.relationship('Question', backref = 'quiz')
    score = db.relationship('Score', backref = 'quiz')
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"), nullable=False)

class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    statement = db.Column(db.Text, nullable = False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False) 
    option_a = db.Column(db.Text, nullable = False)
    option_b = db.Column(db.Text, nullable = False)
    option_c = db.Column(db.Text, nullable = False)
    option_d = db.Column(db.Text, nullable = False)
    correct_answer = db.Column(db.Text, nullable = False)

class Score(db.Model):
    __tablename__ = "score"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False) 
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False) 
    marks = db.Column(db.Integer, nullable=False)  


# 1.  app setup (admin, sqlalchemy, db)
# 2.  models created
# 3.  add data in tables similar to admin
# 4.  boostrap jinja and base template setup 
# 5.  setup flash 
# 6.  create login and register frontend and backend
# 7.  navbar make ----------------
# 8.  admin home show subjects
# 9.  user home ------------------
# 10. cru subjects
# 11. cru quiz or questions 
# 12. delete subject chapter quiz question
# 13. stats (user- best subject, highest marks, subject wise avg marks, weekest chapters,)
# 14. api ----------------------
# 15. user chapter page
# 16. user quiz page
# 17. user question page