from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets

db = SQLAlchemy()

class Utilizador(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nomeUtilizador = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    administrador = db.Column(db.Boolean, default=False)
    api_key = db.Column(db.String(64), unique=True, index=True)
    ativo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Utilizador {self.nomeUtilizador}>"

    def serializar(self):
        return {
            "id": self.id,
            "nomeUtilizador": self.nomeUtilizador,
            "administrador": self.administrador,
            "api_key": self.api_key,
            "ativo": self.ativo,
        }

    def set_password(self, senha):
        self.password = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.password, senha)

    def update_api_key(self):
        # Gera um token hex de 64 caracteres
        self.api_key = secrets.token_hex(32)
