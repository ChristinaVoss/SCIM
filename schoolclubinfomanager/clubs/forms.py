#form imports
from flask_wtf import FlaskForm
from schoolclubinfomanager import db
from schoolclubinfomanager.models import YearGroup, StaffMember, ExternalCompany
from wtforms import StringField,SubmitField, ValidationError, SelectMultipleField, SelectField, TextAreaField, widgets, DateField, DateTimeField, TimeField, BooleanField, RadioField
from wtforms.validators import DataRequired, EqualTo, URL, Length, Regexp, Optional, Email
from flask_wtf.file import FileField, FileAllowed

#school imports
###from flask_login import current_user
from schoolclubinfomanager.models import Club, ClubDay, ClubYearGroup, ContactToBook, ExternalCompany, StaffClub, StaffMember, YearGroup

DAYS = [('Monday', 'Monday'),
         ('Tuesday', 'Tuesday'),
         ('Wednesday', 'Wednesday'),
         ('Thursday', 'Thursday'),
         ('Friday', 'Friday'),
         ('Saturday', 'Saturday'),
         ('Sunday', 'Sunday')]

BOOKING = [('drop_in', 'drop_in'),
           ('teacher', 'teacher'),
           ('email', 'email'),
           ('call', 'call')]

YEAR_GROUPS = sorted([(yg.name, yg.name) for yg in YearGroup.query.all()])
STAFF = [('Choose staff', 'Choose staff')] + sorted([(s.name, s.name) for s in StaffMember.query.all()])
COMPANIES = [('Choose company', 'Choose company')] + sorted([(c.name, c.name) for c in ExternalCompany.query.all()])


# helper class to create checkbox fields (https://gist.github.com/doobeh/4668212)
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

# Flask forms (wtforms) allow you to easily create forms in format:
# variable_name = Field_type('Label that will show', validators=[V_func1(), V_func2(),...])
class CreateClub(FlaskForm):
    # CORE INFORMATION
    name = StringField('Name of club*', validators=[DataRequired(), Length(min=2, max=64)])
    start_date = DateField('Start date (this term)*', validators=[DataRequired()])
    end_date = DateField('End date (this term)*', validators=[DataRequired()])
    end_time = TimeField('End time*', format='%H:%M', validators=[DataRequired()])
    start_time = TimeField('Start time*', format='%H:%M', validators=[DataRequired()])
    location = RadioField('', choices=[('at_school', 'at_school'), ('off_school', 'off_school')])
    at_school_premises = StringField('Please fill in room name/number')
    off_school_premises = TextAreaField('Please provide address')
    days = MultiCheckboxField('Day(s) the club will be running*', choices=DAYS, validators=[DataRequired()])
    #category = RadioField('Category')
    # WHO CAN JOIN
    year_groups = MultiCheckboxField('Year groups you offer clubs to*', choices=YEAR_GROUPS, validators=[DataRequired()])
    experience = StringField('Experience needed to join club')
    outfit = StringField('Please wear')
    equipment = StringField('Please bring')
    num_places = StringField('How many spaces are there available?')
    # BOOKING AND COST
    book = RadioField("Drop in (no need to book)", choices=BOOKING)
    teacher = StringField('Please provide name of teacher to contact:')
    email = StringField('Please provide email to contact:')
    call = StringField('Please provide number to contact:')
    is_free = RadioField('Free', choices=[('free', 'free'), ('paid', 'paid')])
    cost = StringField('Please enter cost per week:')
    # DESCRIPTION OF CLUB AND PHOTO
    photo = FileField('Upload photo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'svg']), Optional()])
    description = TextAreaField('Description of club and/or club activities*')
    #DESCRIPTION OF CLUB LEADER< COMPANY OR STAFF
    #staff_dropdown = SelectField(u'Existing staff members')
    #companies_dropdown = SelectField(u'Existing companies')
    new_entry = RadioField('', choices=[('new', 'new'), ('existing', 'existing')])
    type_of_staff = RadioField('', choices=[('person', 'person'), ('company', 'company')], validators=[Optional()])
    staff_name = StringField('Name of club staff member')
    staff_email = StringField('Email', validators=[Email(), Optional()])
    staff_description = TextAreaField('Description of new staff member')
    company_name = StringField('Name of company')
    company_email = StringField('Email', validators=[Email(), Optional()])
    company_description = TextAreaField('Description of company')
    company_website = StringField('Company website', validators=[URL(), Optional()])
    existing_clubrunner = RadioField('', choices=[('existing_staff', 'existing_staff'), ('existing_company', 'existing_company')], validators=[Optional()])
    staff = SelectField('Staff members - select one', choices=STAFF, validators=[Optional()])
    companies = SelectField('Companies - select one', choices=COMPANIES, validators=[Optional()])
    # SUBMIT FORM
    submit = SubmitField('Save')
    # Not sure how to add more staff members yet (dynamically) - need to look up!

class Publish(FlaskForm):
    publish = SubmitField('Publish')
    unpublish = SubmitField('Unpublish')

class DeleteClub(FlaskForm):
    delete = SubmitField('Delete club')

class EditStaffDetails(FlaskForm):
    name = StringField('Update name')
    email = StringField('Update email', validators=[Email(), Optional()])
    description = TextAreaField('Update descrition of this staff member')
    submit_update = SubmitField('Update details')
    removeStaffFromClub = SubmitField('')
    removeStaff = SubmitField('')

class EditCompanyDetails(FlaskForm):
    name = StringField('Update name')
    email = StringField('Update email', validators=[Email(), Optional()])
    website = StringField('Company website', validators=[URL(), Optional()])
    description = TextAreaField('Update description of this company')
    submit_update = SubmitField('Update details')
    removeCompanyFromClub = SubmitField('')
    removeCompany = SubmitField('')
