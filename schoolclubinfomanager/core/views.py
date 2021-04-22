from flask import Blueprint

core = Blueprint('core', __name__)

# temporary view to check application runs
@core.route('/')
def index():
    return "Core homepage test"
