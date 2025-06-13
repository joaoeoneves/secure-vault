from flask import Blueprint, jsonify, request, make_response
from models import db, Utilizador
from flask_login import login_user, logout_user, current_user

utilizador_bp = Blueprint('utilizador_api', __name__, url_prefix='/api/utilizador')

@utilizador_bp.route('/criar', methods=['POST'])
def criar_utilizador():
    nome = request.form.get('nomeUtilizador')
    senha = request.form.get('password')
    if not nome or not senha:
        return jsonify({"message": "nomeUtilizador e password são obrigatórios."}), 400

    if Utilizador.query.filter_by(nomeUtilizador=nome).first():
        return jsonify({"message": "Utilizador já existe."}), 409

    user = Utilizador(nomeUtilizador=nome)
    user.set_password(senha)
    user.update_api_key()
    db.session.add(user)
    db.session.commit()

    return jsonify(user.serializar()), 201

@utilizador_bp.route('/login', methods=['POST'])
def login():
    nome = request.form.get('nomeUtilizador')
    senha = request.form.get('password')
    user = Utilizador.query.filter_by(nomeUtilizador=nome).first()
    if not user or not user.check_password(senha):
        return jsonify({"message": "Credenciais inválidas."}), 401

    user.update_api_key()
    db.session.commit()
    login_user(user)
    return jsonify({"api_key": user.api_key})

@utilizador_bp.route('/<nomeUtilizador>/existe', methods=['GET'])
def existe_utilizador(nomeUtilizador):
    existe = Utilizador.query.filter_by(nomeUtilizador=nomeUtilizador).first() is not None
    return jsonify({"result": existe}), (200 if existe else 404)

@utilizador_bp.route('/', methods=['GET'])
def utilizador_atual():
    if current_user.is_authenticated:
        return jsonify({"result": current_user.serializar()}), 200
    return jsonify({"message": "Não autenticado."}), 401

@utilizador_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"message": "Logout efetuado."})
