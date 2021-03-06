import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_assets import Environment, Bundle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret' #to allow us to use forms, not safe for deployment

##########################################
############## ASSET SETUP ###############
##########################################

assets = Environment(app)

# create bundle for Flask-Assets to compile and prefix scss to css
css = Bundle('src/scss/main.scss',
             filters=['libsass'],
             output='dist/css/styles.css',
             depends='src/scss/*/*/*.scss')

assets.register("asset_css", css)
css.build()

##########################################
############ DATABASE SETUP ##############
##########################################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

##########################################
######### LOGIN CONFIGURATION ############
##########################################

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

##########################################
######### REGISTER BLUEPRINTS ############
##########################################

from schoolclubinfomanager.core.views import core
from schoolclubinfomanager.school.views import school
from schoolclubinfomanager.users.views import users
from schoolclubinfomanager.clubs.views import clubs

app.register_blueprint(core)
app.register_blueprint(clubs)
app.register_blueprint(school)
app.register_blueprint(users)
