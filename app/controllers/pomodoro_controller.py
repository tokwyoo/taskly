from flask import Blueprint, redirect, render_template, session, url_for

pomodoro_bp = Blueprint("pomodoro", __name__)

@pomodoro_bp.route("/pomodoro")
def pomodoro():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("pomodoro.html")