from app.db import db
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "user"  # Nombre exacto de la tabla en PostgreSQL

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    email_verified = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.String(255), nullable=True)
    verified = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "email_verified": self.email_verified,
            "profile_picture": self.profile_picture,
            "bio": self.bio,
            "verified": self.verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def set_password(self, password):
        """Genera un hash de la contraseña y lo guarda"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con la almacenada"""
        return check_password_hash(self.password, password)
