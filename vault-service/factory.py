from entries.password import PasswordEntryCreator
from entries.credit_card import CreditCardEntryCreator
from entries.note import NoteEntryCreator
from entries.ssh_key import SSHKeyEntryCreator

class EntryFactory:
    creators = {
        'password': PasswordEntryCreator(),
        'credit_card': CreditCardEntryCreator(),
        'note': NoteEntryCreator(),
        'ssh_key': SSHKeyEntryCreator(),
    }

    @staticmethod
    def create_entry(entry_type, user_id, title, **kwargs):
        creator = EntryFactory.creators.get(entry_type)
        if not creator:
            raise ValueError(f"Tipo desconhecido: {entry_type}")
        return creator.create(user_id=user_id, title=title, **kwargs)
