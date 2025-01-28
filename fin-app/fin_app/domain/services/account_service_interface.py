from abc import ABC


class AccountServiceInterface(ABC):

    def get_all(self):
        pass

    def get_by_id(self, id):
        pass

    def create(self, data):
        pass
