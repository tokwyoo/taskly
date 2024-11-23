import os

class Config:
    # Secret Key para sesiones y csrf
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-secreta-muy-dificil-de-adivinar'

    # Datos de conexión
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "taskly_bd"
    DB_USER = "myuser"
    DB_PASSWORD = "mypassword"

    # Construcción de las URLs de conexión
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SQLALCHEMY_ASYNC_DATABASE_URI = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # Opciones adicionales
    SQLALCHEMY_ECHO = True  # Cambia a False en producción

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SCSS_FOLDER = os.path.join(BASE_DIR, 'static', 'scss')
    CSS_FOLDER = os.path.join(BASE_DIR, 'static', 'css')