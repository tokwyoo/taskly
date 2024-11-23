from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import db
from app.models.user import User
from werkzeug.security import generate_password_hash
import re

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=['GET'])
def register():
    return render_template("register.html")

@auth_bp.route("/register", methods=['POST'])
def register_post():
    try:
        # Obtener datos del formulario
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        terms = request.form.get('terms')
        
        # Validaciones
        if not all([email, name, password, repassword, terms]):
            flash('All fields are required', 'error')
            return redirect(url_for('auth.register'))

        # Validar longitud del nombre
        if len(name) < 2 or len(name) > 50:
            flash('Name must be between 2 and 50 characters', 'error')
            return redirect(url_for('auth.register'))

        # Validar formato de email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            flash('Please enter a valid email address', 'error')
            return redirect(url_for('auth.register'))

        # Validar contraseña
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return redirect(url_for('auth.register'))

        if password != repassword:
            flash('Passwords do not match', 'error')
            return redirect(url_for('auth.register'))

        # Verificar si el email ya está registrado
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email is already registered', 'error')
            return redirect(url_for('auth.register'))

        # Crear nuevo usuario
        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            email_verified=False,
            verified=False
        )

        # Guardar en la base de datos
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please sign in', 'success')
        return redirect(url_for('auth.login'))

    except Exception as e:
        db.session.rollback()
        flash('An error occurred during registration. Please try again.', 'error')
        return redirect(url_for('auth.register'))

@auth_bp.route("/login", methods=['GET'])
def login():
    return render_template("login.html")