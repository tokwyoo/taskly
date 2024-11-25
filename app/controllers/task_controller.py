from flask import Blueprint, redirect, render_template, request, jsonify, abort, session, url_for
from app.models.task import Task
from app.models.list import List
from app.db import db
from datetime import datetime

from app.models.user import User

tasks = Blueprint('tasks', __name__)

@tasks.route('/lists/<int:list_id>/tasks')
def index(list_id):
    ##### ACCESO RESTRINGIDO
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
        
    list_obj = List.query.get_or_404(list_id)
    
    if list_obj.is_deleted:
        abort(404)
        
    if list_obj.user_id != session["user_id"]:
        abort(403)
    
    if list_obj.user_id != session["user_id"]:
        abort(403)  
    ##### ACCESO RESTRINGIDO
    
    # Obtener el usuario y las tareas
    user = User.query.get(session["user_id"])    
    tasks = Task.query.filter_by(list_id=list_id, is_deleted=False).all()
    
    return render_template('tasks.html', user=user, list=list_obj, tasks=tasks)

@tasks.route('/lists/<int:list_id>/tasks', methods=['POST'])
def create(list_id):
    ##### ACCESO RESTRINGIDO
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
        
    list_obj = List.query.get_or_404(list_id)
    
    if list_obj.is_deleted:
        abort(404)
        
    if list_obj.user_id != session["user_id"]:
        abort(403)
    
    if list_obj.user_id != session["user_id"]:
        abort(403)  
    ##### ACCESO RESTRINGIDO
    
    """Crea una nueva tarea en la lista especificada"""
    list_obj = List.query.get_or_404(list_id)
    if list_obj.is_deleted:
        abort(404)
        
    data = request.get_json()
    
    task = Task(
        list_id=list_id,
        title=data['title'],
        notes=data.get('notes'),
        due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict())

@tasks.route('/lists/<int:list_id>/tasks/<int:task_id>', methods=['PUT'])
def update(list_id, task_id):
    ##### ACCESO RESTRINGIDO
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
        
    list_obj = List.query.get_or_404(list_id)
    
    if list_obj.is_deleted:
        abort(404)
        
    if list_obj.user_id != session["user_id"]:
        abort(403)
    
    if list_obj.user_id != session["user_id"]:
        abort(403)  
    ##### ACCESO RESTRINGIDO
    
    """Actualiza una tarea existente"""
    task = Task.query.filter_by(id=task_id, list_id=list_id).first_or_404()
    if task.is_deleted:
        abort(404)
        
    data = request.get_json()
    
    task.title = data['title']
    task.notes = data.get('notes')
    task.due_date = datetime.fromisoformat(data['due_date']) if data.get('due_date') else None
    
    db.session.commit()
    
    return jsonify(task.to_dict())

@tasks.route('/lists/<int:list_id>/tasks/<int:task_id>', methods=['DELETE'])
def delete(list_id, task_id):
    ##### ACCESO RESTRINGIDO
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
        
    list_obj = List.query.get_or_404(list_id)
    
    if list_obj.is_deleted:
        abort(404)
        
    if list_obj.user_id != session["user_id"]:
        abort(403)
    
    if list_obj.user_id != session["user_id"]:
        abort(403)  
    ##### ACCESO RESTRINGIDO
    
    """Realiza un borrado suave de una tarea"""
    task = Task.query.filter_by(id=task_id, list_id=list_id).first_or_404()
    
    task.soft_delete()
    db.session.commit()
    
    return jsonify({'message': 'Task deleted successfully'})

@tasks.route('/lists/<int:list_id>/tasks/<int:task_id>/toggle', methods=['PUT'])
def toggle_complete(list_id, task_id):
    ##### ACCESO RESTRINGIDO
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
        
    list_obj = List.query.get_or_404(list_id)
    
    if list_obj.is_deleted:
        abort(404)
        
    if list_obj.user_id != session["user_id"]:
        abort(403)
    
    if list_obj.user_id != session["user_id"]:
        abort(403)  
    ##### ACCESO RESTRINGIDO
    
    """Cambia el estado de completado de una tarea"""
    task = Task.query.filter_by(id=task_id, list_id=list_id).first_or_404()
    if task.is_deleted:
        abort(404)
    
    if task.is_completed:
        task.uncomplete()
    else:
        task.complete()
    
    db.session.commit()
    
    return jsonify(task.to_dict())

@tasks.route('/lists/<int:list_id>/tasks/<int:task_id>/restore', methods=['PUT'])
def restore(list_id, task_id):
    ##### ACCESO RESTRINGIDO
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
        
    list_obj = List.query.get_or_404(list_id)
    
    if list_obj.is_deleted:
        abort(404)
        
    if list_obj.user_id != session["user_id"]:
        abort(403)
    
    if list_obj.user_id != session["user_id"]:
        abort(403)  
    ##### ACCESO RESTRINGIDO
    
    """Restaura una tarea que fue eliminada mediante borrado suave"""
    task = Task.query.filter_by(id=task_id, list_id=list_id).first_or_404()
    
    task.restore()
    db.session.commit()
    
    return jsonify(task.to_dict())

# Endpoint adicional para actualizar la frecuencia de una tarea
@tasks.route('/lists/<int:list_id>/tasks/<int:task_id>/frequency', methods=['PUT'])
def update_frequency(list_id, task_id):
    
    ##### ACCESO RESTRINGIDO
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
        
    list_obj = List.query.get_or_404(list_id)
    
    if list_obj.is_deleted:
        abort(404)
        
    if list_obj.user_id != session["user_id"]:
        abort(403)
    
    if list_obj.user_id != session["user_id"]:
        abort(403)  
    ##### ACCESO RESTRINGIDO

    """Actualiza la frecuencia de una tarea"""
    task = Task.query.filter_by(id=task_id, list_id=list_id).first_or_404()
    if task.is_deleted:
        abort(404)
    
    data = request.get_json()
    task.update_frequency(data)
    
    db.session.commit()
    
    return jsonify(task.to_dict())