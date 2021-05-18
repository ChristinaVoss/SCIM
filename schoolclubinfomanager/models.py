from schoolclubinfomanager import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#########################################
######### USER RELATED MODELS ###########
#########################################

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    # initialise an instance (row) of a table/entity
    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # __repr__ is used to represent an instance, such as for print() function
    def __repr__(self):
        return f"Name: {self.name}, Email: {self.email}"

#########################################
######### SCHOOL RELATED MODELS #########
#########################################

class School(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    club_summary = db.Column(db.Text)
    logo = db.Column(db.String(64))
    num_clubs = db.Column(db.Integer, nullable=False)
    banner_colour = db.Column(db.String(7))
    font_colour = db.Column(db.String(7))
    font = db.Column(db.String(64))
    website = db.Column(db.String(64))
    yeargroups = db.relationship("YearGroup", back_populates="school")
    #tokens = db.relationship('ApproveNewUserToken', back_populates="school")

    def __init__(self, name, club_summary, logo, website):
        self.name = name
        self.club_summary = club_summary
        self.logo = logo
        self.website = website
        self.num_clubs = 0
        self.banner_colour = "#19456b"
        self.font_colour = "FFFFFF"

    def __repr__(self):
        return f"{self.name}"

class YearGroup(db.Model):
    __tablename__= 'yeargroups'

    school_id = db.Column(db.Integer, ForeignKey(School.id), primary_key=True)
    name = db.Column(db.String(20), primary_key=True)
    school = db.relationship("School", back_populates="yeargroups")

    def __init__(self, name, school_id):
        self.name = name
        self.school_id = school_id

#https://stackoverflow.com/questions/44941757/sqlalchemy-exc-operationalerror-sqlite3-operationalerror-no-such-table

#########################################
######### CLUB RELATED MODELS ###########
#########################################

class ContactToBook(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True)
    call = db.Column(db.String(64), unique=True, index=True)
    clubs = db.relationship("Club", back_populates="contacts_to_book")

    def __init__(self, teacher_name=None, email=None, call=None):
        self.teacher_name = teacher_name
        self.email = email
        self.call = call

class ExternalCompany(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    website = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    description = db.Column(db.String(500))
    clubs = db.relationship("Club", back_populates="external_company")

    def __init__(self, name, website, email, description):
        self.name = name
        self.website = website
        self.email = email
        self.description = description

    def __repr__(self):
        return f"{self.name}"

class Club(db.Model):
    __tablename__= 'clubs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(64)) # add nullable=False when you have categories from School setup/filter setup
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    at_school = db.Column(db.Boolean, nullable=False)
    experience = db.Column(db.String(120))
    equipment = db.Column(db.String(120))
    outfit = db.Column(db.String(120))
    is_free = db.Column(db.Boolean, nullable=False)
    cost = db.Column(db.Integer)#store as pennies - convert with code
    photo = db.Column(db.String(64))
    description = db.Column(db.String(500))
    time_of_day = db.Column(db.Integer, nullable=False)
    num_of_places = db.Column(db.Integer, nullable=False)
    drop_in = db.Column(db.Boolean, nullable=False)
    contacts_to_book = db.relationship("ContactToBook", back_populates="clubs")
    contact_to_book_id = db.Column(db.Integer, ForeignKey(ContactToBook.id))
    ext_company_id = db.Column(db.Integer, ForeignKey(ExternalCompany.id))
    external_company = db.relationship("ExternalCompany", back_populates="clubs")
    clubdays = db.relationship("ClubDay", back_populates="club")
    club_yeargroups = db.relationship("ClubYearGroup", back_populates="club")
    staffclubs = db.relationship("StaffClub", back_populates="club")

    # initialise an instance (row) of a table/entity
    def __init__(self, name, start_date, end_date, start_time, end_time,
                 location, at_school, is_free, num_of_places, drop_in):

        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.at_school = at_school
        self.is_free = is_free
        self.num_of_places = num_of_places
        self.drop_in = drop_in

    def __repr__(self):
        return f"{self.name}"


class ClubDay(db.Model):

    club_id = db.Column(db.Integer, ForeignKey(Club.id), primary_key=True)
    name = db.Column(db.String(64), primary_key=True)
    club = db.relationship("Club", back_populates="clubdays")

    def __init__(self, name, club_id):
        self.name = name
        self.club_id = club_id


class ClubYearGroup(db.Model):

    club_id = db.Column(db.Integer, ForeignKey(Club.id), primary_key=True)
    name = db.Column(db.String(64), primary_key=True)
    club = db.relationship("Club", back_populates="club_yeargroups")

    def __init__(self, name, club_id):
        self.name = name
        self.club_id = club_id


class StaffMember(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, index=True)
    description = db.Column(db.String(500))
    staffclubs = db.relationship("StaffClub", back_populates="staffmember")

    def __init__(self, name, website, email, description):
        self.name = name
        self.website = website
        self.email = email
        self.description = description

    def __repr__(self):
        return f"{self.name}"

# Composite entity to join clubs and staff members 
class StaffClub(db.Model):

    club_id = db.Column(db.Integer, ForeignKey(Club.id), primary_key=True)
    staffmember_id = db.Column(db.Integer, ForeignKey(StaffMember.id), primary_key=True)
    club = db.relationship("Club", back_populates="staffclubs")
    staffmember = db.relationship("StaffMember", back_populates="staffclubs")

    def __init__(self, club_id, staffmember_id):
        self.club_id = club_id
        self.staffmember_id = staffmember_id



db.create_all()
'''
class ApproveNewUserToken(db.Model):

    school_id = db.Column(db.Integer, ForeignKey(School.id), primary_key=True)
    token = db.Column(db.String(128), unique=True, primary_key=True)
    issued_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    school = db.relationship("School", back_populates="tokens")

    def __init__(self, school_id, token, issued_time):
        self.school_id = school_id
        self.token = token
        self.issued_time = issued_time

    def __repr__(self):
        return f"{self.token}"'''
