from flask import Blueprint, flash, request, render_template, redirect, url_for
from models import User,db, Admin, Subject
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from utils import bcrypt

auth = Blueprint("auth", __name__)

@auth.route("/register_user", methods = ["GET", "POST"])
def register_user():
    if request.method == "POST":
        form_username = request.form.get("form_username")
        form_password = request.form.get("form_password")
        form_qualification = request.form.get("form_qualification")
        form_dob = request.form.get("form_dob")

        user = User.query.filter_by(username = form_username).first()
        if user:
            flash("User already exists!")
            return redirect(url_for("auth.login"))

        dob_obj = datetime.strptime(form_dob, "%Y-%m-%d").date()

        password = bcrypt.generate_password_hash(form_password).decode("utf-8")
       
        new_user = User(username = form_username,
                        password = password, 
                        qualification = form_qualification, 
                        dob = dob_obj)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successfull!", category= "success")
        return redirect(url_for("auth.login"))
    return render_template("register_user.html")

# @auth.route("/register_user", methods=["GET", "POST"])
# def register_user():
#     if request.method == "POST":
#         form_username = request.form.get("form_username")
#         form_password = request.form.get("form_password")
#         form_qualification = request.form.get("form_qualification")
#         form_dob = request.form.get("form_dob")

#         user = User.query.filter_by(username=form_username).first()
#         if user:
#             flash("User already exists!")
#             return redirect(url_for("auth.login"))

#         dob_obj = datetime.strptime(form_dob, "%Y-%m-%d").date()

#         # Generate password hash with bcrypt and decode to store as a string
#         hashed_password = bcrypt.generate_password_hash(form_password).decode("utf-8")
#         new_user = User(
#             username=form_username,
#             password=hashed_password,
#             qualification=form_qualification,
#             dob=dob_obj
#         )
#         db.session.add(new_user)
#         db.session.commit()
#         flash("Registration successful!", category="success")
#         return redirect(url_for("auth.login"))
#     return render_template("register_user.html")

@auth.route("/", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        form_username = request.form.get("form_username")
        form_password = request.form.get("form_password")

        user = User.query.filter_by(username = form_username).first()
        admin = Admin.query.filter_by(username = form_username).first()
        if user:
            if bcrypt.check_password_hash(user.password, form_password):
                flash("Logged in successfully!", category= 'success')
                return redirect(url_for("user.user_home", user_id = user.id))
            else:
                flash("Incorrect password, try logging in again!", category= 'error')
        elif admin:
            if Admin.query.filter_by(password = form_password):
                flash("Logged in successfully!", category= "success")
                return redirect(url_for("admin.admin_home"))
            else:
                flash("Incorrect password, try logging in again!", category= 'error')
        else:
            flash("Username does not exist, register!")
            return redirect(url_for("auth.register_user"))
    return render_template("login.html")

# @auth.route('/logout')
# # @login_required
# def logout():
#     logout_user
#     return redirect(url_for('auth.login'))