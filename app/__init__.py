# app/__init__.py

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os
import json

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

from app.models.user     import User
from app.models.student  import Student
from app.models.teacher  import Teacher
from app.models.writer   import Writer
from app.models.class_ import Class
from app.models.subject  import Subject
from app.models.grade    import Grade
from app.models.article  import Article
from app.models.teacher_junction import teacher_subject, teacher_class

from app.services.user_services import create_user,get_user_by_username

migrate = Migrate()

# user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Create the config.json file if it doesn't exist
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            default_cfg = {"language": "en", "SECRET_KEY": "super-secret-dev-key", "DATABASE_URI": "sqlite:///../instance/school.db", "first_load": True}
            json.dump(default_cfg, f)

    # Load config
    with open(config_path) as f:
        config = json.load(f)

    app.config['SECRET_KEY'] = config.get('SECRET_KEY', 'dev_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get('DATABASE_URI', 'sqlite:///../instance/school.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.teacher import teacher_bp
    from app.routes.student import student_bp
    from app.routes.writer import writer_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(writer_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    migrate.init_app(app, db)
    print("[INFO] Database migration initialized.")
    # Create the database if it doesn't exist
    if not os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'instance', 'school.db')) and config.get('first_load'):
        with app.app_context():
            db.create_all()
            print("[INFO] Database created.")
    if config.get('first_load'):
        # Create an admin user
        with app.app_context():
            if not get_user_by_username('admin'):
                create_user(
                    username='admin',
                    password='admin',
                    role='admin')
                print("[INFO] Admin user created.")
            else:
                print("[INFO] Admin user already exists.")
    config['first_load'] = False
    with open(config_path, 'w') as f:
        json.dump(config, f)
    print("[INFO] Config updated.")
    
    return app
