from flask import render_template, url_for, redirect, request, Blueprint, session
from flask_login import login_user, current_user, logout_user, login_required
from schoolclubinfomanager import db
from schoolclubinfomanager.models import User, School

core = Blueprint('core', __name__)

# temporary view to check application runs
@core.route('/')
def index():

    #school = School.query.first()

    #return render_template('base.html', school=school)
    return redirect(url_for('users.login'))
