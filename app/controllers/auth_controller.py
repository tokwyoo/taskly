from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from app.db import db
from app.models.user import User
from werkzeug.security import check_password_hash
import re

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET"])
def register():
    if "user_id" in session:
        return redirect(url_for("home.home"))
    return render_template("register.html")


@auth_bp.route("/register", methods=["POST"])
def register_post():
    try:
        # Obtener datos del formulario
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")
        repassword = request.form.get("repassword")
        terms = request.form.get("terms")

        # Validaciones
        if not all([email, name, password, repassword, terms]):
            flash("All fields are required", "error")
            return redirect(url_for("auth.register"))

        # Validar longitud del nombre
        if len(name) < 2 or len(name) > 50:
            flash("Name must be between 2 and 50 characters", "error")
            return redirect(url_for("auth.register"))

        # Validar formato de email
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            flash("Please enter a valid email address", "error")
            return redirect(url_for("auth.register"))

        # Validar contraseña
        if len(password) < 6:
            flash("Password must be at least 6 characters long", "error")
            return redirect(url_for("auth.register"))

        if password != repassword:
            flash("Passwords do not match", "error")
            return redirect(url_for("auth.register"))

        # Verificar si el email ya está registrado
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email is already registered", "error")
            return redirect(url_for("auth.register"))

        # Crear nuevo usuario
        new_user = User(
            name=name,
            email=email,
            email_verified=False,
            verified=False,
        )

        # Establecer la contraseña de forma segura
        new_user.set_password(password)

        # Guardar en la base de datos
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please sign in", "success")
        return redirect(url_for("auth.login"))

    except Exception as e:
        db.session.rollback()
        flash("An error occurred during registration. Please try again.", "error")
        return redirect(url_for("auth.register"))


@auth_bp.route("/login", methods=["GET"])
def login():
    if "user_id" in session:
        return redirect(url_for("home.home"))
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login_post():
    try:
        # Obtener datos del formulario
        email = request.form.get("email")
        password = request.form.get("password")

        # Validaciones
        if not all([email, password]):
            flash("All fields are required", "error")
            return redirect(url_for("auth.login"))

        # Buscar usuario por email
        user = User.query.filter_by(email=email).first()

        # Verificar si el usuario existe y la contraseña es correcta
        if user:
            if check_password_hash(user.password, password):
                session["user_id"] = user.id  # Guardar el ID del usuario en la sesión
                session['user_name'] = user.name
                flash("Login successful!", "success")
                return redirect(url_for("home.home"))
            else:
                flash("Invalid email or password", "error")
                return redirect(url_for("auth.login"))
        else:
            flash("Invalid email or password", "error")
            return redirect(url_for("auth.login"))

    except Exception as e:
        # flash(f"An error occurred during login. Please try again. Error: {str(e)}", "error")
        flash(f"An error occurred during login. Please try again.")
        return redirect(url_for("auth.login"))


@auth_bp.route("/logout", methods=["POST"])
def logout_post():
    try:
        # Eliminar los datos de sesión (esto cierra la sesión del usuario)
        session.pop(
            "user_id", None
        )  # Suponiendo que guardas el ID del usuario en la sesión

        # Limpiar cualquier mensaje flash previo
        session.pop("_flashes", None)

        flash("You have been logged out successfully.", "success")
        return redirect(url_for("auth.login"))

    except Exception as e:
        # En caso de error, mostrar el mensaje correspondiente
        flash(
            f"An error occurred during logout. Please try again. Error: {str(e)}",
            "error",
        )
        return redirect(url_for("home.home"))
