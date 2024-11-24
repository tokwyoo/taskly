from flask import Blueprint, redirect, render_template, session, url_for

from app.models.user import User

lists_bp = Blueprint("lists", __name__)

@lists_bp.route("/lists")
def lists():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    user = User.query.get(session["user_id"])
    return render_template("lists.html", user=user)