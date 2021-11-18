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
    # return redirect(url_for('root'))
    return render_template("index.html", logout=True)


@auth.route('/update_username', methods=["POST"])
def update_username():
    update_username_form = request.form
    ori_name = update_username_form["ori-name"]
    new_name = update_username_form["new-name"]
    try:
        update_uname(ori_name, new_name)
    except Exception as err:
        print(err)
        return render_template("home.html", update_username_result="failure")
    return render_template("home.html", update_username_result="success")


@auth.route('/home')
def home():
    if 'email' in session:
        return render_template('home.html', user_email=session['email'], user_name=session["user_name"])
    else:
        return redirect(url_for('/login'))