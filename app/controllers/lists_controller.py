from flask import Blueprint, redirect, render_template, session, url_for

lists_bp = Blueprint("lists", __name__)

@lists_bp.route("/lists")
def lists():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("lists.html")