from flask import Blueprint, redirect, request, session, render_template, url_for
from OOTD.views.database import *


auth = Blueprint('auth', __name__)


# register
@auth.route('/register', methods=["POST"])
def register():
    user_info = request.form
    email = user_info["register_email"]
    password = user_info["register_password"]
    gender = user_info["register_gender"]
    name = user_info["register_name"]
    dob = user_info["register_dob"]
    try:
        add_user(email, gender, password, name, dob)
    except Exception as err:
        print(err)
        return render_template("index.html", register_failed=True)
    return render_template("index.html", register_success=True)


# login
@auth.route('/login', methods=["GET", "POST"])
def login():
    email = request.form["input_email"]
    password = request.form["input_password"]
    if is_valid(email, password):
        session['email'] = email
        session['user_name'] = find_user(email)
        return redirect(url_for('auth.home'))
    else:
        return render_template('login.html', login_failed=True)


# logout
@auth.route('/logout')
def logout():
    session.pop('email', None)
    return render_template("index.html", logout=True)


@auth.route('/update_user_info', methods=["POST"])
def update_user_info():
    update_user_form = request.form
    new_name = update_user_form["new-name"]
    new_password = update_user_form["new-password"]
    email = session['email']
    try:
        update_user(new_name, new_password, email)
    except Exception as err:
        print(err)
        return render_template("home.html", update_user_result="failure")
    return render_template("home.html", update_user_result="success")


@auth.route('/home')
def home():
    if 'email' in session:
        return render_template('home.html', user_email=session['email'], user_name=session["user_name"])
    else:
        return redirect(url_for('/login'))