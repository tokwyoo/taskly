from flask import Blueprint, redirect, render_template, session, url_for

search_bp = Blueprint("search", __name__)

@search_bp.route("/search")
def search():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("search.html")