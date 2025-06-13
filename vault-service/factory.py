from models import BaseEntry

class EntryFactory:
    @staticmethod
    def create_entry(entry_type, user_id, title, **kwargs):
        data = {}
        if entry_type == 'password':
            data = {'username': kwargs.get('username'), 'password': kwargs.get('password')}
        elif entry_type == 'credit_card':
            data = {
                'card_number': kwargs.get('card_number'),
                'expiry_date': kwargs.get('expiry_date'),
                'cvv': kwargs.get('cvv')
            }
        elif entry_type == 'ssh_key':
            data = {'ssh_key': kwargs.get('ssh_key')}
        elif entry_type == 'note':
            data = {'note_text': kwargs.get('note_text')}
        else:
            raise ValueError(f"Tipo desconhecido: {entry_type}")
        return BaseEntry(user_id=user_id, type=entry_type, title=title, data=data)
