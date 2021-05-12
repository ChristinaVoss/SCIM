from flask import render_template, url_for, redirect, request, Blueprint, session
from flask_login import login_user, current_user, logout_user, login_required
from schoolclubinfomanager import db
from schoolclubinfomanager.models import User, School
from schoolclubinfomanager.users.forms import RegistrationForm, LoginForm, UpdateUserForm, DeleteUserForm

users = Blueprint('users', __name__)

# REGISTER
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    school = School.query.first() # base template needs this variable
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    name = form.name.data,
                    password = form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    return (render_template('register.html', form=form, school=school))

# LOGIN
@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    school = School.query.first() # base template needs this variable
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)

            school = School.query.all()

            if not school:
                return redirect(url_for('school.setup_step1'))
            else:
                return redirect(url_for('school.school_account'))
    return render_template('login.html', form=form, school=school) # this return is connected to the overall form - check indentaion!

# LOGOUT
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))


# LIST USERS
@users.route('/list_users')
@login_required
def list_users():
    users = User.query.all()
    school = School.query.first() # base tempalte needs this variable
    return render_template('admin/list_users.html', users=users, school=school)

# EDIT USERS
@users.route('/user_account', methods=["GET", "POST"])
@login_required
def user_account():
    school = School.query.first() # base tempalte needs this variable
    form = UpdateUserForm()
    if form.validate_on_submit():

        current_user.name = form.name.data
        current_user.email = form.email.data


        db.session.commit()
        return redirect(url_for('users.user_account'))
    elif request.method == "GET":
        # they are not really submitting anything and we grab their current name and Email
        form.name.data = current_user.name
        form.email.data = current_user.email

    return render_template('admin/user_account.html', form=form, school=school)


# DELETE USER
@users.route('/delete_user/<user>', methods=['GET', 'POST'])
@login_required
def delete_user(user):
    # MUST CREATE MORE CHECKS - YOU SHOULD BE ABLE TO DELETE LAST USER! (OR YOURSELF?)

    user = User.query.filter_by(id=user).first()
    form = DeleteUserForm()
    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        # user has pressed "Delete user button,
        # so delete user and return to list"
        return redirect(url_for('users.list_users'))
    # when user first enters page, this is inital view
    return render_template('admin/delete_user.html', form=form, user=user)
