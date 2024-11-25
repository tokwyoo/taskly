from flask import abort, redirect, session, url_for

from app.models.list import List
from app.models.task import Task


def check_list_ownership(list_id):
    """
    Verifica si el usuario actual es el propietario de la lista.
    Redirige al login si no hay sesión, lanza 403 si no es propietario.
    """
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    list_obj = List.query.get_or_404(list_id)
    if list_obj.user_id != session["user_id"]:
        abort(403)

    return list_obj


def check_task_ownership(task_id):
    """
    Verifica si el usuario actual es el propietario de la lista de la tarea.
    Redirige al login si no hay sesión, lanza 403 si no es propietario.
    """
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    task = Task.query.get_or_404(task_id)
    if task.list.user_id != session["user_id"]:
        abort(403)

    return task