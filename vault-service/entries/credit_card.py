from entries.base import EntryCreator
from models import BaseEntry
from crypto import encrypt

class CreditCardEntryCreator(EntryCreator):
    def create(self, user_id, title, **kwargs):
        data = {
            'card_number': kwargs.get('card_number'),
            'expiry_date': kwargs.get('expiry_date'),
            'cvv': kwargs.get('cvv')
        }
        return BaseEntry(user_id=user_id, type='credit_card', title=title, data=encrypt(data))
