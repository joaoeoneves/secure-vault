from abc import ABC, abstractmethod

# Classe abstrata base para criadores de entradas (usada no padrão Factory)
class EntryCreator(ABC):
    @abstractmethod
    def create(self, user_id, title, **kwargs):
        pass
