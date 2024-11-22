from flask import Flask
from app.config import Config
from app.utils.scss_utils import compile_all_scss
from app.utils.db import init_db
import asyncio
from app.controllers.auth_controller import auth_bp
from app.controllers.home_controller import home_bp

def create_app():
    app = Flask(__name__)

    # Cargar configuración
    app.config.from_object(Config)

    # Inicializar la conexión a la base de datos
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db(app))

    # Compilar SCSS
    compile_all_scss(app.config['SCSS_FOLDER'], app.config['CSS_FOLDER'])

   # Registrar Blueprints sin url_prefix
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)

    return app
