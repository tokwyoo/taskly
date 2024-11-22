from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There! - Taskly App</h1>"
