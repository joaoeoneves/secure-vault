from flask import Blueprint, jsonify, request
from flask_login import login_user
from flask_login import current_user
from facade import UtilizadorFacade

# Blueprint para agrupar as rotas relacionadas com utilizadores.
# Facilita a organização e integração com a aplicação principal.
utilizador_bp = Blueprint('utilizador_api', __name__, url_prefix='/api/utilizador')

# Rota para criar um novo utilizador.
# Usa a fachada para encapsular a lógica de criação.
@utilizador_bp.route('/criar', methods=['POST'])
def criar_utilizador():
    nome = request.form.get('nomeUtilizador')
    senha = request.form.get('password')
    if not nome or not senha:
        return jsonify({"message": "nomeUtilizador e password são obrigatórios."}), 400

    user, erro = UtilizadorFacade.criar_utilizador(nome, senha)
    if erro:
        return jsonify({"message": erro}), 409

    return jsonify(user.serializar()), 201

# Rota para login de utilizador.
# Autentica e devolve a API key.
@utilizador_bp.route('/login', methods=['POST'])
def login():
    nome = request.form.get('nomeUtilizador')
    senha = request.form.get('password')
    user = UtilizadorFacade.autenticar_utilizador(nome, senha)
    if not user:
        return jsonify({"message": "Credenciais inválidas."}), 401

    login_user(user)
    return jsonify({"api_key": user.api_key})

# Rota para verificar se um utilizador existe.
@utilizador_bp.route('/<nomeUtilizador>/existe', methods=['GET'])
def existe_utilizador(nomeUtilizador):
    existe = UtilizadorFacade.existe_utilizador(nomeUtilizador)
    return jsonify({"result": existe}), (200 if existe else 404)

# Rota para obter o utilizador autenticado (usada por outros serviços).
@utilizador_bp.route('/', methods=['GET'])
def utilizador_atual():
    if current_user.is_authenticated:
        return jsonify({"result": current_user.serializar()}), 200
    return jsonify({"message": "Não autenticado."}), 401

# Rota para logout.
@utilizador_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"message": "Logout efetuado."})
