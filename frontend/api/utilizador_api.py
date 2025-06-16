import requests
from flask import session
from . import UTILIZADOR_API_URL

# Classe para interagir com o serviço de utilizadores (user-service)
class UtilizadorApi:
    @staticmethod
    def login(form):
        # Envia pedido de login ao user-service
        payload = {
            'nomeUtilizador': form.nomeUtilizador.data,
            'password': form.password.data,
        }
        url = f"{UTILIZADOR_API_URL}/api/utilizador/login"
        resp = requests.post(url, data=payload)
        if resp.status_code == 200:
            return resp.json().get('api_key')
        return None

    @staticmethod
    def criar_Utilizador(form):
        # Envia pedido de criação de utilizador ao user-service
        payload = {
            'nomeUtilizador': form.nomeUtilizador.data,
            'password': form.password.data,
        }
        url = f"{UTILIZADOR_API_URL}/api/utilizador/criar"
        resp = requests.post(url, data=payload)
        if resp.status_code == 201:
            return resp.json()
        return None

    @staticmethod
    def existe(nome):
        # Verifica se o utilizador já existe
        url = f"{UTILIZADOR_API_URL}/api/utilizador/{nome}/existe"
        resp = requests.get(url)
        return resp.status_code == 200
