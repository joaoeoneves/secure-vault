from database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets

# Modelo de dados para o utilizador.
# Herda de UserMixin para integração com Flask-Login.
class Utilizador(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nomeUtilizador = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    administrador = db.Column(db.Boolean, default=False)
    api_key = db.Column(db.String(64), unique=True, index=True)
    ativo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Utilizador {self.nomeUtilizador}>"

    # Serializa o utilizador para dicionário (útil para respostas JSON)
    def serializar(self):
        return {
            "id": self.id,
            "nomeUtilizador": self.nomeUtilizador,
            "administrador": self.administrador,
            "api_key": self.api_key,
            "ativo": self.ativo,
        }

    # Guarda a password de forma segura (hash)
    def set_password(self, senha):
        self.password = generate_password_hash(senha)

    # Verifica se a password fornecida está correta
    def check_password(self, senha):
        return check_password_hash(self.password, senha)

    # Gera uma nova API key para o utilizador (autenticação por token)
    def update_api_key(self):
        self.api_key = secrets.token_hex(32)
