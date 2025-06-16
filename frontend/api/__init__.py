import os

# Endpoints das APIs externas (user-service e vault-service)
UTILIZADOR_API_URL = os.getenv('UTILIZADOR_API_URL', 'http://localhost:5001')
VAULT_API_URL       = os.getenv('VAULT_API_URL',       'http://localhost:5002')
