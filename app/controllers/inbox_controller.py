from flask import Blueprint, redirect, render_template, session, url_for

from app.models.user import User

inbox_bp = Blueprint("inbox", __name__)

@inbox_bp.route("/inbox")
def inbox():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    user = User.query.get(session["user_id"])
    return render_template("inbox.html", user=user)