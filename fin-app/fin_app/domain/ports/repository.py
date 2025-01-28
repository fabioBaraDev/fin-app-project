from abc import ABC

from fin_app.domain.entities import AccountDomain


class AccountRepositoryInterface(ABC):
    def get_all(self) -> list[AccountDomain]:
        pass

    def get_by_id(self, id) -> AccountDomain:
        pass

    def create(self, acc: AccountDomain) -> AccountDomain:
        pass
