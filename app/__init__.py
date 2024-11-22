from flask import Flask, render_template
from app.utils.scss_utils import compile_all_scss
from app.config import Config

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    compile_all_scss(app.config['SCSS_FOLDER'], app.config['CSS_FOLDER'])

    @app.route("/")
    def hello():
        return "<h1 style='color:blue'>Hello There! - Taskly App</h1>"
    
    @app.route("/register")
    def register():
        return render_template('register.html')

    return app