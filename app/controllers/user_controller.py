from flask import Blueprint, redirect, render_template, session, url_for

user_bp = Blueprint("user", __name__)

@user_bp.route("/settings")
def settings():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("settings.html")