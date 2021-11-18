from flask import Blueprint, redirect, request, session, render_template
from OOTD.views.database import *

auth = Blueprint('auth', __name__)


@auth.route('/')
def page():
    return "<h1>Authentication</h1>"


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
        # return redirect(url_for('root'))
        return render_template('index.html', login_success=True)
    else:
        return render_template('index.html', login_failed=True)


# logout
@auth.route('/logout')
def logout():
    session.pop('email', None)
    # return redirect(url_for('root'))
    return render_template("index.html", logout=True)