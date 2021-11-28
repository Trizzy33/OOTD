from flask import Blueprint, redirect, request, session, render_template, url_for, flash
from OOTD.views.database import *
from OOTD.settings import app, gcached_table
import json
import os

auth = Blueprint('auth', __name__)


@auth.route('/home')
def home():
    if 'email' in session:
        print(gcached_table)
        print(session["ucached_table"])
        item_data = get_rank_products(session["ucached_table"])
        return render_template('index.html', loggedIn=True, user_name=session["user_name"], item_data=item_data)
    else:
        return redirect(url_for('main.home'))

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


# login form
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
        path = os.path.join(app.config["PREFERENCES_DIR"], email + ".json")
        session["ucached_table"] = {}
        if os.path.isfile(path):
            with open(path, "r") as f:
                session["ucached_table"] = json.load(f)
        flash("Login Successfully")
        return redirect(url_for('auth.home'))
    else:
        error_msg = "Invalid User Name/Password!"
        return render_template('login.html', error=error_msg)


# logout
@auth.route('/logout')
def logout():
    email = session["email"]
    path = os.path.join(app.config["PREFERENCES_DIR"], email + ".json")
    with open(path, "w+") as fp:
        json.dump(session["ucached_table"], fp)
    session.pop("ucached_table", None)
    session.pop('email', None)
    flash("Logout Successfully!")
    return redirect(url_for('auth.home'))


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
    if update_password(old_password, new_password, email):
        flash("Successfully Changed!")
        return redirect(url_for('auth.home'))
    else:
        flash("Failed")
    return render_template("password.html", msg="Wrong password")


# get user profile
@auth.route("/profile")
def profile_form():
    if 'email' not in session:
        return redirect(url_for('login_form'))
    else:
        email = session['email']
        profile_data = get_user_info(email)
    return render_template("profile.html", profileData=profile_data, email=email)


# update user profile
@auth.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
    user_profile = request.form
    email = user_profile['email']
    name = user_profile['user_name']
    gender = user_profile['gender']
    dob = user_profile['user_dob']
    try:
        update_user(email, name, gender, dob)
        flash("Profile Updated!")
        return redirect(url_for('auth.home'))
    except Exception as err:
        print(err)
    return redirect(url_for('auth.profile_form'))

