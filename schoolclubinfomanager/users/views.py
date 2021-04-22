from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from schoolclubinfomanager import db
from schoolclubinfomanager.models import User
from schoolclubinfomanager.users.forms import RegistrationForm, LoginForm

users = Blueprint('users', __name__)

# REGISTER
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    name = form.name.data,
                    password = form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    return (render_template('register.html', form=form))


@users.route('/login')
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            next = request.args.get('next') # grabs info about where the user was trying to access prior to login

            if next == None or not next[0] == '/':
                next = url_for('core.index')

            return redirect(next) # this return is connected to the if user.check_password statement
        return render_template('login.html', form=form) # this return is connected to the overall form - check indentaion!
        
