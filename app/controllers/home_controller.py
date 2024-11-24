from flask import Blueprint, render_template, redirect, url_for, flash, session

from app.models.user import User

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    user = User.query.get(session["user_id"])
    return render_template("home.html", user=user)
