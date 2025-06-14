from entries.base import EntryCreator
from models import BaseEntry
from crypto import encrypt

class SSHKeyEntryCreator(EntryCreator):
    def create(self, user_id, title, **kwargs):
        data = {
            'ssh_key': kwargs.get('ssh_key')
        }
        return BaseEntry(user_id=user_id, type='ssh_key', title=title, data=encrypt(data))
