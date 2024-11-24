from flask import Blueprint, redirect, render_template, session, url_for

from app.models.user import User

trash_bp = Blueprint("trash", __name__)

@trash_bp.route("/trash")
def trash():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    user = User.query.get(session["user_id"])
    return render_template("trash.html", user=user)