from flask import Blueprint, render_template

writer_bp = Blueprint('writer', __name__, url_prefix='/writer')