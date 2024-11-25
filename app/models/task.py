from app.db import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = "task"  # Nombre exacto de la tabla en PostgreSQL

    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    frequency = db.Column(db.JSON, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Relación con el modelo List
    list = db.relationship('List', backref=db.backref('tasks', lazy=True))

    def __repr__(self):
        return f"<Task {self.title}>"

    def to_dict(self):
        return {
            "id": self.id,
            "list_id": self.list_id,
            "title": self.title,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "frequency": self.frequency,
            "notes": self.notes,
            "is_completed": self.is_completed,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "is_deleted": self.is_deleted,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None
        }

    def complete(self):
        """Marca la tarea como completada"""
        self.is_completed = True
        self.completed_at = datetime.utcnow()

    def uncomplete(self):
        """Desmarca la tarea como completada"""
        self.is_completed = False
        self.completed_at = None

    def soft_delete(self):
        """Realiza un borrado suave de la tarea"""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()

    def restore(self):
        """Restaura una tarea que fue borrada suavemente"""
        self.is_deleted = False
        self.deleted_at = None

    def update_frequency(self, frequency_data):
        """Actualiza la frecuencia de la tarea"""
        self.frequency = frequency_data