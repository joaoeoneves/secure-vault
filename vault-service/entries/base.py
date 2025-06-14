from abc import ABC, abstractmethod

class EntryCreator(ABC):
    @abstractmethod
    def create(self, user_id, title, **kwargs):
        pass
