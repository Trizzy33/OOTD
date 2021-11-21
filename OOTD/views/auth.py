from flask import Blueprint, redirect, request, session, render_template, url_for, flash
from OOTD.views.database import *


auth = Blueprint('auth', __name__)


# register
@auth.route('/register', methods=["POST"])
def register():
    error_msg = ''
    user_info = request.form
    email = user_info["register_email"]
    password = user_info["register_password"]
    conform_password = user_info["conform_password"]
    gender = user_info["register_gender"]
    name = user_info["register_name"]
    dob = user_info["register_dob"]
    if gender not in ['MALE', 'FEMALE']:
        error_msg = "Invalid Gender"
        return render_template("register.html", error=error_msg)
    if conform_password != password:
        error_msg = "Password Not Match"
        return render_template("register.html", error=error_msg)
    try:
        add_user(email, gender, password, name, dob)
    except Exception as err:
        print(err)
        error_msg = 'Error Occurred'
        return render_template("register.html", error=error_msg)
    return render_template("login.html", error='')


@auth.route("/register_form")
def register_form():
    return render_template("register.html", error='')


@auth.route("/login_form")
def login_form():
    if 'email' in session:
        return redirect(url_for('auth.home'))
    else:
        return render_template('login.html', error='')


# login
@auth.route('/login', methods=["GET", "POST"])
def login():
    error_msg = ' '
    email = request.form["input_email"]
    password = request.form["input_password"]
    if is_valid(email, password):
        session['email'] = email
        session['user_name'] = find_user(email)
        return redirect(url_for('auth.home'))
    else:
        error_msg = "Invalid User Name/Password!"
        return render_template('login.html', error=error_msg)


# logout
@auth.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('auth.home'))
    # return render_template("index1.html", logout=True)


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
        return render_template('index.html', loggedIn=True, user_name=session["user_name"])
    else:
        return render_template('index.html', loggedIn=False)


@auth.route("/password")
def password_form():
    if 'email' not in session:
        return redirect(url_for('login_form'))
    else:
        return render_template("password.html", msg='')


@auth.route("/change_password", methods=['GET', 'POST'])
def change_password():
    if 'email' not in session:
        return redirect(url_for('login_form'))
    change_password_form = request.form
    old_password = change_password_form['old_password']
    new_password = change_password_form['new_password']
    email = session['email']
    try:
        if update_password(old_password, new_password, email):
            flash("Successfully Changed!")
            redirect(url_for('auth.home'))
        else:
            flash("Failed")
    except Exception as err:
        print(err)
        return render_template("password.html", msg="Error")
    return render_template("password.html", msg="Wrong password")
