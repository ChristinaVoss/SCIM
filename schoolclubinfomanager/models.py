from schoolclubinfomanager import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

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
