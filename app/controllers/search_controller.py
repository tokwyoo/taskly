from flask import Blueprint, redirect, render_template, session, url_for

from app.models.user import User

search_bp = Blueprint("search", __name__)

@search_bp.route("/search")
def search():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    user = User.query.get(session["user_id"])
    return render_template("search.html", user=user)