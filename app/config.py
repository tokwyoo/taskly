# app/config.py
import os

class Config:

    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "taskly_bd"
    DB_USER = "myuser"
    DB_PASSWORD = "mypassword"

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SCSS_FOLDER = os.path.join(BASE_DIR, 'static', 'scss')
    CSS_FOLDER = os.path.join(BASE_DIR, 'static', 'css')
