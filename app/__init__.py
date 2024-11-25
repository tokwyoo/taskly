# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # Asegúrate de importar SQLAlchemy
from app.config import Config
from app.utils.scss_utils import compile_all_scss
from app.controllers.auth_controller import auth_bp
from app.controllers.home_controller import home_bp
from app.controllers.inbox_controller import inbox_bp
from app.controllers.lists_controller import lists_bp
from app.controllers.pomodoro_controller import pomodoro_bp
from app.controllers.search_controller import search_bp
from app.controllers.trash_controller import trash_bp
from app.controllers.user_controller import user_bp
from app.controllers.task_controller import tasks_bp
from app.db import db

def create_app():
    app = Flask(__name__)

    # Cargar configuración desde Config
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    # Compilar SCSS
    compile_all_scss(app.config['SCSS_FOLDER'], app.config['CSS_FOLDER'])

    # Registrar Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(inbox_bp)
    app.register_blueprint(lists_bp)
    app.register_blueprint(pomodoro_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(trash_bp)
    app.register_blueprint(tasks_bp)

    return app
