from flask import Blueprint, redirect, render_template, session, url_for

inbox_bp = Blueprint("inbox", __name__)

@inbox_bp.route("/inbox")
def inbox():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("inbox.html")