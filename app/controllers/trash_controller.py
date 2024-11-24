from flask import Blueprint, redirect, render_template, session, url_for

trash_bp = Blueprint("trash", __name__)

@trash_bp.route("/trash")
def trash():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("trash.html")