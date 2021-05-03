from flask import render_template, url_for, redirect, request, Blueprint, session
from flask_login import login_user, current_user, logout_user, login_required
from schoolclubinfomanager import db
from schoolclubinfomanager.models import School, YearGroup
from schoolclubinfomanager.school.forms import SchoolSetupStep1, SchoolSetupStep2
from schoolclubinfomanager.school.picture_handler import add_logo

school = Blueprint('school', __name__)

# SETUP STEP 1
@school.route('/setup1', methods=['GET', 'POST'])
def setup_step1():
    form = SchoolSetupStep1()

    if form.validate_on_submit():
        # first setup step collects core school information

        # save logo
        if form.logo.data: #if they actually uploaded a logo
            if form.name.data: # if they filled in a name
                school_name = form.name.data
                school_name = school_name.replace(' ', '')
                pic = add_logo(form.logo.data, school_name)
            else:
                pic = add_logo(form.logo.data, "school")
        else:
            pic = None

        school = School(name=form.name.data,
                        club_summary = form.summary.data,
                        logo = pic,
                        website = form.school_website.data)

        db.session.add(school)
        db.session.commit()
        #update database with year groups
        year_groups = form.year_groups.data
        for group in year_groups:
            yg = YearGroup(group, school.id)
            db.session.add(yg)

        db.session.commit()
        return redirect(url_for('school.setup_step2', school=school.id))
    return (render_template('admin/setup_step1.html', form=form))


# SETUP STEP 2
@school.route('/setup2/<school>', methods=['GET', 'POST'])
def setup_step2(school):
    form = SchoolSetupStep2()
    school = School.query.filter_by(id=school).first()
    if form.validate_on_submit():
        # this setup step collects information on colours and looks for parent side banner



        school.banner_colour = form.banner_colour.data
        school.font_colour = form.font_colour.data
        school.font = form.font.data

        db.session.commit()
        return redirect(url_for('school.school_account'))
    return (render_template('admin/setup_step2.html', form=form, school=school))


# HOME
@school.route('/school_account', methods=['GET'])
def school_account():
    school = School.query.all()
    #year_groups = YearGroup.query.filter_by(school_id=school.id)
    #return render_template('admin/school_account.html', school=school, year_groups=year_groups)
    return render_template('admin/school_account.html', school=school)
