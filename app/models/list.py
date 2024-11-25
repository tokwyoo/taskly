from app.db import db
from datetime import datetime

class List(db.Model):
    __tablename__ = "list"  # Nombre exacto de la tabla en PostgreSQL

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Relación con el modelo User
    user = db.relationship('User', backref=db.backref('lists', lazy=True))

    def __repr__(self):
        return f"<List {self.title}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_deleted": self.is_deleted,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None
        }
    
    def soft_delete(self):
        """Realiza un borrado suave de la lista"""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()

    def restore(self):
        """Restaura una lista que fue borrada suavemente"""
        self.is_deleted = False
        self.deleted_at = None