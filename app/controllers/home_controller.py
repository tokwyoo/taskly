import datetime  # Esto importa el módulo datetime
from flask import Blueprint, render_template, redirect, url_for, session
import requests
import time
from app.models.user import User
from app.models.task import Task  # Asegúrate de importar el modelo Task

home_bp = Blueprint("home", __name__)

# Variables globales para la cita y el tiempo de la última actualización
current_quote = None
current_author = None
last_updated = 0
QUOTE_REFRESH_INTERVAL = 600  # 10 minutos en segundos


def get_inspirational_quote():
    """
    Devuelve una cita inspiradora, actualizándola si ha pasado más tiempo que el intervalo.
    """
    global current_quote, current_author, last_updated

    if time.time() - last_updated > QUOTE_REFRESH_INTERVAL:
        try:
            response = requests.get("http://api.quotable.io/random?tags=inspirational")
            quote_data = response.json()
            current_quote = quote_data['content']
            current_author = quote_data['author']
            last_updated = time.time()
        except Exception:
            current_quote = "No se pudo obtener una cita hoy."
            current_author = "Sistema"
    
    return current_quote, current_author


@home_bp.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    user = User.query.get(session["user_id"])

    # Obtener la cita inspiradora
    quote, author = get_inspirational_quote()

    # Obtener las tareas del usuario, filtrando por user_id de la lista y excluyendo las eliminadas
    tasks = Task.query.filter(Task.list.has(user_id=user.id), Task.is_deleted == False).all()

    # Obtener las tareas categorizadas
    today = datetime.datetime.now().date()  # Usa datetime.datetime.now() en lugar de datetime.now()

    # Ordenar las tareas por due_date de más antigua a más futura
    overdue_tasks = sorted([task for task in tasks if task.due_date and task.due_date.date() < today and not task.is_completed], key=lambda t: t.due_date)
    today_tasks = sorted([task for task in tasks if task.due_date and task.due_date.date() == today and not task.is_completed], key=lambda t: t.due_date)
    upcoming_tasks = sorted([task for task in tasks if task.due_date and task.due_date.date() > today and not task.is_completed], key=lambda t: t.due_date)
    completed_tasks = sorted([task for task in tasks if task.is_completed], key=lambda t: t.completed_at if t.completed_at else t.created_at)

    # Saludo genérico como fallback
    greeting = "Hello there"
    
    return render_template("home.html", 
                           user=user, 
                           quote=quote, 
                           author=author, 
                           greeting=greeting,
                           overdue_tasks=overdue_tasks,
                           today_tasks=today_tasks,
                           upcoming_tasks=upcoming_tasks,
                           completed_tasks=completed_tasks)
