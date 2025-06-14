import requests
from . import VAULT_API_URL

class VaultApi:
    @staticmethod
    def get_entries(api_key):
        r = requests.get(f"{VAULT_API_URL}/api/vault/entries",
                         headers={'Authorization': api_key})
        return r.json() if r.status_code == 200 else []

    @staticmethod
    def create_entry(api_key, data):
        r = requests.post(
            f"{VAULT_API_URL}/api/vault/entries",
            headers={'Authorization': api_key},
            json=data
        )
        return r.status_code == 201

    @staticmethod
    def update_entry(api_key, entry_id, data):
        r = requests.put(
            f"{VAULT_API_URL}/api/vault/entries/{entry_id}",
            headers={'Authorization': api_key},
            json=data
        )
        return r.status_code == 200

    @staticmethod
    def delete_entry(api_key, entry_id):
        r = requests.delete(
            f"{VAULT_API_URL}/api/vault/entries/{entry_id}",
            headers={'Authorization': api_key}
        )
        return r.status_code == 200

    @staticmethod
    def get_health(api_key, entry_id):
        r = requests.get(
            f"{VAULT_API_URL}/api/vault/entries/{entry_id}/health",
            headers={'Authorization': api_key}
        )
        return r.json() if r.status_code == 200 else {"status": "error", "reason": "Erro ao avaliar saúde"}
