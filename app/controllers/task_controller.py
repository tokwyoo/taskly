from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
)
from app.models.task import Task
from app.db import db
from datetime import datetime
from app.utils.ownership_utils import check_list_ownership, check_task_ownership

from app.models.user import User

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("/lists/<int:list_id>/tasks")
def view_tasks(list_id):

    current_list = check_list_ownership(list_id)

    today = datetime.now().date()

    tasks = Task.query.filter_by(list_id=list_id, is_deleted=False).all()

    overdue_tasks = [
        task
        for task in tasks
        if task.due_date and not task.is_completed and task.due_date.date() < today
    ]

    today_tasks = [
        task
        for task in tasks
        if task.due_date and not task.is_completed and task.due_date.date() == today
    ]

    upcoming_tasks = [
        task
        for task in tasks
        if task.due_date and not task.is_completed and task.due_date.date() > today
    ]

    completed_tasks = [task for task in tasks if task.is_completed]

    user = User.query.get(session["user_id"])

    return render_template(
        "tasks.html",
        user=user,
        list=current_list,
        overdue_tasks=overdue_tasks,
        today_tasks=today_tasks,
        upcoming_tasks=upcoming_tasks,
        completed_tasks=completed_tasks,
    )


@tasks_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = check_task_ownership(task_id)
    return jsonify(task.to_dict()), 200


@tasks_bp.route("/tasks/<int:task_id>", methods=["PUT", "DELETE"])
def manage_task(task_id):
    task = check_task_ownership(task_id)

    if request.method == "PUT":
        data = request.json
        task.title = data.get("title", task.title)
        task.due_date = (
            datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None
        )
        task.notes = data.get("notes", task.notes)
        db.session.commit()
        return jsonify(task.to_dict()), 200

    elif request.method == "DELETE":
        task.soft_delete()
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"}), 200


@tasks_bp.route("/tasks/<int:task_id>/complete", methods=["POST"])
def complete_task(task_id):
    task = check_task_ownership(task_id)
    task.complete()
    db.session.commit()
    return jsonify(task.to_dict()), 200


@tasks_bp.route("/tasks/<int:task_id>/uncomplete", methods=["POST"])
def uncomplete_task(task_id):
    task = check_task_ownership(task_id)
    task.uncomplete()
    db.session.commit()
    return jsonify(task.to_dict()), 200


@tasks_bp.route("/lists/<int:list_id>/tasks", methods=["POST"])
def create_task(list_id):
    check_list_ownership(list_id)

    data = request.json
    new_task = Task(
        list_id=list_id,
        title=data["title"],
        due_date=(
            datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None
        ),
        notes=data.get("notes"),
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201
