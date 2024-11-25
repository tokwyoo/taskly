from flask import abort, session

from app.models.list import List
from app.models.task import Task


def check_list_ownership(list_id):
    """
    Verifica si el usuario actual es el propietario de la lista.
    Lanza un 403 Forbidden si no lo es.
    """
    if "user_id" not in session:
        abort(403)

    list_obj = List.query.get_or_404(list_id)
    if list_obj.user_id != session["user_id"]:
        abort(403)

    return list_obj


def check_task_ownership(task_id):
    """
    Verifica si el usuario actual es el propietario de la lista a la que pertenece la tarea.
    Lanza un 403 Forbidden si no lo es.
    """
    if "user_id" not in session:
        abort(403)

    task = Task.query.get_or_404(task_id)
    if task.list.user_id != session["user_id"]:
        abort(403)

    return task