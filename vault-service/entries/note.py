from entries.base import EntryCreator
from models import BaseEntry
from crypto import encrypt

# Criador de entradas do tipo "note"
class NoteEntryCreator(EntryCreator):
    def create(self, user_id, title, **kwargs):
        data = {
            'note_text': kwargs.get('note_text')
        }
        return BaseEntry(user_id=user_id, type='note', title=title, data=encrypt(data))
