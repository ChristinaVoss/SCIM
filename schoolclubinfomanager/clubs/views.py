from flask import render_template, url_for, redirect, request, Blueprint, session
from flask_login import login_user, current_user, logout_user, login_required
from schoolclubinfomanager import db
from schoolclubinfomanager.models import School, YearGroup, Club, ClubDay, ClubYearGroup, ContactToBook, StaffClub, StaffMember
from schoolclubinfomanager.clubs.forms import CreateClub
from schoolclubinfomanager.school.picture_handler import add_logo
import datetime

clubs = Blueprint('clubs', __name__)

# SETUP STEP 1
@clubs.route('/create_club', methods=['GET', 'POST'])
@login_required
def create_club():
    form = CreateClub()
    school = School.query.first()
    # for validating datepickers:
    today = datetime.date.today()
    one_year = str(datetime.datetime.now())[:10]
    one_year = one_year[:3] + str(int(one_year[3]) + 1) + one_year[4:10]

    #school = School.query.first()
    if form.validate_on_submit():
        pass

    return (render_template('admin/club_form.html', form=form, title="Create", school=school, today=today, one_year=one_year))
