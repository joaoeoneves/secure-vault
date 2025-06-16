import requests
from . import VAULT_API_URL

# Classe para interagir com o serviço de cofre (vault-service)
class VaultApi:
    @staticmethod
    def get_entries(api_key):
        # Obtém todas as entradas do cofre do utilizador autenticado
        r = requests.get(f"{VAULT_API_URL}/api/vault/entries",
                         headers={'Authorization': api_key})
        return r.json() if r.status_code == 200 else []

    @staticmethod
    def create_entry(api_key, data):
        # Cria uma nova entrada no cofre
        r = requests.post(
            f"{VAULT_API_URL}/api/vault/entries",
            headers={'Authorization': api_key},
            json=data
        )
        return r.status_code == 201

    @staticmethod
    def update_entry(api_key, entry_id, data):
        # Atualiza uma entrada existente
        r = requests.put(
            f"{VAULT_API_URL}/api/vault/entries/{entry_id}",
            headers={'Authorization': api_key},
            json=data
        )
        return r.status_code == 200

    @staticmethod
    def delete_entry(api_key, entry_id):
        # Apaga uma entrada do cofre
        r = requests.delete(
            f"{VAULT_API_URL}/api/vault/entries/{entry_id}",
            headers={'Authorization': api_key}
        )
        return r.status_code == 200

    @staticmethod
    def get_health(api_key, entry_id):
        # Avalia a "saúde" (segurança) de uma entrada
        r = requests.get(
            f"{VAULT_API_URL}/api/vault/entries/{entry_id}/health",
            headers={'Authorization': api_key}
        )
        return r.json() if r.status_code == 200 else {"status": "error", "reason": "Erro ao avaliar saúde"}
