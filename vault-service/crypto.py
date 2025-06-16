import os
import base64
import json
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

# Gera um objeto Fernet para encriptação/decifração simétrica
def get_fernet():
    secret = os.getenv("SECRET_KEY", "superSecretKey").encode()
    key = base64.urlsafe_b64encode(secret.ljust(32, b'0')[:32])
    return Fernet(key)

# Encripta um dicionário para string
def encrypt(data_dict):
    f = get_fernet()
    json_data = json.dumps(data_dict).encode()
    encrypted = f.encrypt(json_data)
    return encrypted.decode()

# Desencripta uma string para dicionário
def decrypt(encrypted_str):
    f = get_fernet()
    decrypted = f.decrypt(encrypted_str.encode())
    return json.loads(decrypted.decode())
