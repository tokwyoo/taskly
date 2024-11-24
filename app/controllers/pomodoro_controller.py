from flask import Blueprint, redirect, render_template, session, url_for

from app.models.user import User

pomodoro_bp = Blueprint("pomodoro", __name__)

@pomodoro_bp.route("/pomodoro")
def pomodoro():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    user = User.query.get(session["user_id"])
    return render_template("pomodoro.html", user=user)