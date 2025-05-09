from flask import Blueprint, render_template
from flask_login import current_user, login_required

student_bp = Blueprint('student', __name__, url_prefix='/student')

@login_required
@student_bp.route('/')
def index():
    return render_template('student/index.html')

@login_required
@student_bp.route('/grades')
def grades():
    return "work in progress"