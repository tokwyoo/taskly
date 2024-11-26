from flask import Blueprint, jsonify, redirect, render_template, session, url_for
from app.models.user import User
from app.models.task import Task
from app.models.list import List
from app.db import db

trash_bp = Blueprint("trash", __name__)

@trash_bp.route("/trash")
def trash():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    user = User.query.get(session["user_id"])

    tasks_in_trash = Task.query.filter(Task.list.has(user_id=user.id), Task.is_deleted == True) \
    .order_by(Task.deleted_at.desc()).all()


    return render_template("trash.html", tasks_in_trash=tasks_in_trash, user=user)

@trash_bp.route("/trash/restore/<int:task_id>", methods=["POST"])
def restore_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    task = Task.query.get_or_404(task_id)

    # Verificar si el usuario tiene permisos sobre la tarea (a través de la lista asociada)
    if task.list.user_id != session["user_id"]:
        return jsonify({"error": "Forbidden"}), 403
    
    # Restaurar la tarea
    task.restore()

    # Si la lista asociada a la tarea está eliminada, restaurarla también
    if task.list and task.list.is_deleted:
        task.list.restore()

    db.session.commit()

    return redirect(url_for('trash.trash'))  # Redirige de vuelta a la papelera 

@trash_bp.route("/trash/delete_forever/<int:task_id>", methods=["POST"])
def delete_forever(task_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    task = Task.query.get_or_404(task_id)

    # Verificar si el usuario tiene permisos sobre la tarea (a través de la lista asociada)
    if task.list.user_id != session["user_id"]:
        return jsonify({"error": "Forbidden"}), 403
    
    # Eliminar la tarea permanentemente
    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('trash.trash'))  # Redirige de vuelta a la papelera
