from entries.base import EntryCreator
from models import BaseEntry
from crypto import encrypt

# Criador de entradas do tipo "password"
class PasswordEntryCreator(EntryCreator):
    def create(self, user_id, title, **kwargs):
        data = {
            'username': kwargs.get('username'),
            'password': kwargs.get('password')
        }
        return BaseEntry(user_id=user_id, type='password', title=title, data=encrypt(data))
