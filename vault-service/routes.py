from flask import Blueprint, request, jsonify, abort
from database import db
from factory import EntryFactory
from models import BaseEntry
import os
import requests

vault_bp = Blueprint('vault_api', __name__, url_prefix='/api/vault')

def authenticate():
    api_key = request.headers.get('Authorization')
    if not api_key:
        abort(401, 'Missing Authorization header')
    user_url = os.getenv('UTILIZADOR_API_URL', 'http://user-service:5001')
    resp = requests.get(f"{user_url}/api/utilizador/", headers={'Authorization': api_key})
    if resp.status_code != 200:
        abort(401, 'Invalid API key')
    return resp.json()['result']

@vault_bp.route('/entries', methods=['GET'])
def list_entries():
    user = authenticate()
    entries = BaseEntry.query.filter_by(user_id=user['id']).all()
    return jsonify([e.to_dict() for e in entries])

@vault_bp.route('/entries', methods=['POST'])
def create_entry():
    user = authenticate()
    payload = request.get_json()

    entry_type = payload.get('type')
    title      = payload.get('title')
    data       = {k: v for k, v in payload.items() if k not in ('type', 'title')}

    entry = EntryFactory.create_entry(
        entry_type,
        user_id=user['id'],
        title=title,
        **data
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.to_dict()), 201

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

    new_entry = EntryFactory.create_entry(
        entry_type,
        user_id=user['id'],
        title=title,
        **data
    )
    existing.data = new_entry.data

    db.session.commit()
    return jsonify(existing.to_dict())

@vault_bp.route('/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    user = authenticate()
    entry = BaseEntry.query.get_or_404(entry_id)
    if entry.user_id != user['id']:
        abort(404)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({'message': 'Deleted'})
