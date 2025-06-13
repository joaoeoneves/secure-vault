import requests
from flask import session
from . import UTILIZADOR_API_URL

class UtilizadorApi:
    @staticmethod
    def login(form):
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
        url = f"{UTILIZADOR_API_URL}/api/utilizador/{nome}/existe"
        resp = requests.get(url)
        return resp.status_code == 200
