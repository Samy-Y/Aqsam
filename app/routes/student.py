from flask import Blueprint, render_template

student_bp = Blueprint('student', __name__, url_prefix='/student')