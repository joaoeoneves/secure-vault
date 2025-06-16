from flask import Blueprint, request, jsonify, abort
from database import db
from factory import EntryFactory
from models import BaseEntry
import os
import requests

# Blueprint para agrupar as rotas da API do vault
vault_bp = Blueprint('vault_api', __name__, url_prefix='/api/vault')

# Função auxiliar para autenticar o utilizador via API key
def authenticate():
    api_key = request.headers.get('Authorization')
    if not api_key:
        abort(401, 'Missing Authorization header')
    user_url = os.getenv('UTILIZADOR_API_URL', 'http://user-service:5001')
    # Valida a API key junto do user-service
    resp = requests.get(f"{user_url}/api/utilizador/", headers={'Authorization': api_key})
    if resp.status_code != 200:
        abort(401, 'Invalid API key')
    return resp.json()['result']

# Lista todas as entradas do utilizador autenticado
@vault_bp.route('/entries', methods=['GET'])
def list_entries():
    user = authenticate()
    entries = BaseEntry.query.filter_by(user_id=user['id']).all()
    return jsonify([e.to_dict() for e in entries])

# Cria uma nova entrada no cofre usando o padrão Factory
@vault_bp.route('/entries', methods=['POST'])
def create_entry():
    user = authenticate()
    payload = request.get_json()

    entry_type = payload.get('type')
    title      = payload.get('title')
    data       = {k: v for k, v in payload.items() if k not in ('type', 'title')}

    # Usa a EntryFactory para criar a entrada correta consoante o tipo
    entry = EntryFactory.create_entry(
        entry_type,
        user_id=user['id'],
        title=title,
        **data
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.to_dict()), 201

# Atualiza uma entrada existente
@vault_bp.route('/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    user = authenticate()
    existing = BaseEntry.query.get_or_404(entry_id)
    if existing.user_id != user['id']:
        abort(404)

    payload = request.get_json()
    entry_type = payload.get('type')
    title      = payload.get('title')
    data       = {k: v for k, v in payload.items() if k not in ('type', 'title')}

    existing.type  = entry_type
    existing.title = title

    # Cria nova entrada (dados encriptados) e substitui os dados antigos
    new_entry = EntryFactory.create_entry(
        entry_type,
        user_id=user['id'],
        title=title,
        **data
    )
    existing.data = new_entry.data

    db.session.commit()
    return jsonify(existing.to_dict())

# Apaga uma entrada do cofre
@vault_bp.route('/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    user = authenticate()
    entry = BaseEntry.query.get_or_404(entry_id)
    if entry.user_id != user['id']:
        abort(404)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({'message': 'Deleted'})

# Avalia a "saúde" de uma entrada (ex: força da password)
@vault_bp.route('/entries/<int:entry_id>/health', methods=['GET'])
def entry_health(entry_id):
    user = authenticate()
    all_entries = BaseEntry.query.filter_by(user_id=user['id']).all()
    target = next((e for e in all_entries if e.id == entry_id), None)
    if not target:
        abort(404)
    payload = {
        "entry": target.to_dict(),
        "all_entries": [e.to_dict() for e in all_entries]
    }
    # Chama o serviço externo de health-check
    try:
        resp = requests.post(
            "http://health-service:5003/api/health/check",
            json=payload
        )
        return jsonify(resp.json()), resp.status_code
    except Exception:
        return jsonify({"status": "error", "reason": "Erro ao contactar health-service"}), 500
