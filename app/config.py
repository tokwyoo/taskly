# app/config.py
import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SCSS_FOLDER = os.path.join(BASE_DIR, 'static', 'scss')
    CSS_FOLDER = os.path.join(BASE_DIR, 'static', 'css')
