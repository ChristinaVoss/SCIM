from flask import render_template, url_for, redirect, request, Blueprint, session
from flask_login import login_user, current_user, logout_user, login_required
from schoolclubinfomanager import db
from schoolclubinfomanager.models import School, YearGroup
from schoolclubinfomanager.school.forms import SchoolSetupStep1, SchoolSetupStep2
from schoolclubinfomanager.school.picture_handler import add_logo

school = Blueprint('school', __name__)

# SETUP STEP 1
@school.route('/setup1', methods=['GET', 'POST'])
@login_required
def setup_step1():
    form = SchoolSetupStep1()

    #school = School.query.first()
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
    return (render_template('admin/school_details_step1.html', form=form, title="Set up", step_state1="active", step_state2="", line_state=""))


# SETUP STEP 2
@school.route('/setup2/<school>', methods=['GET', 'POST'])
@login_required
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
    return (render_template('admin/school_details_step2.html', form=form, school=school, title="Set up", step_state1="active", step_state2="active", line_state="active"))


# HOME
@school.route('/school_account', methods=['GET'])
@login_required
def school_account():
    school = School.query.first()
    ygs = YearGroup.query.all()
    '''
    for yg in ygs:
        db.session.delete(yg)


    for s in school:
        db.session.delete(s)
    db.session.commit()
    '''
    #year_groups = YearGroup.query.filter_by(school_id=school.id)
    #return render_template('admin/school_account.html', school=school, year_groups=year_groups)
    return render_template('admin/school_account.html', school=school, year_groups=ygs)


#EDIT SCHOOL DETAILS STEP1
@school.route('/edit-school-details-step1', methods=['GET', 'POST'])
@login_required
def edit_step1():
    form = SchoolSetupStep1()
    school = School.query.first()
    year_groups = YearGroup.query.all()
    existing_yg = {yg.name for yg in year_groups}

    if form.validate_on_submit():

        # save logo
        if form.logo.data: #if they actually uploaded a logo
            school_name = form.name.data
            school_name = school_name.replace(' ', '')
            school.logo = add_logo(form.logo.data, school_name)

        school.name = form.name.data
        school.club_summary = form.summary.data
        school.website = form.school_website.data

        db.session.commit()
        #update database with year groups
        new_year_groups = set(form.year_groups.data)
        for group in new_year_groups:
            if group not in existing_yg:
                yg = YearGroup(group, school.id)
                db.session.add(yg)

        to_delete = existing_yg - new_year_groups
        if to_delete:
            for yg in to_delete:
                temp = YearGroup.query.filter_by(name = yg).first()
                db.session.delete(temp)

        db.session.commit()
        return redirect(url_for('school.edit_step2', school=school.id))
    elif request.method == "GET":
        # they are not really submitting anything and we grab their current details
        form.name.data = school.name
        form.summary.data = school.club_summary
        form.school_website.data = school.website
        form.year_groups.data = existing_yg

    return (render_template('admin/school_details_step1.html', form=form, title="Edit", school=school, step_state1="active", step_state2="", line_state=""))

# EDIT SCHOOL DETAILS STEP 2
@school.route('/edit-school-details-step2/<school>', methods=['GET', 'POST'])
@login_required
def edit_step2(school):
    form = SchoolSetupStep2()
    school = School.query.filter_by(id=school).first()
    if form.validate_on_submit():
        # this setup step collects information on colours and looks for parent side banner
        school.banner_colour = form.banner_colour.data
        school.font_colour = form.font_colour.data
        school.font = form.font.data

        db.session.commit()
        return redirect(url_for('school.school_account'))

    elif request.method == "GET":

        form.banner_colour.data = school.banner_colour
        form.font_colour.data = school.font_colour
        form.font.data = school.font
    return (render_template('admin/school_details_step2.html', form=form, school=school, title="Edit", step_state1="active", step_state2="active", line_state="active"))
