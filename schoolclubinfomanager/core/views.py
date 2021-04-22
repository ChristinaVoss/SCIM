#from schoolclubinfomanager import 
from flask import render_template, request, Blueprint

core = Blueprint('core', __name__)

# temporary view to check application runs
@core.route('/')
def index():
    return render_template('base.html')
