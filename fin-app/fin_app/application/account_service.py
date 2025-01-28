from fin_app.domain.entities import AccountDomain
from fin_app.domain.ports.repository import AccountRepositoryInterface
from fin_app.domain.services.account_service_interface import AccountServiceInterface


class AccountService(AccountServiceInterface):
    def __init__(self, repository: AccountRepositoryInterface):
        self.repository = repository

    def get_all(self) -> list[AccountDomain]:
        return self.repository.get_all()

    def get_by_id(self, id) -> AccountDomain:
        return self.repository.get_by_id(id)

    def create(self, acc: AccountDomain) -> AccountDomain:
        return self.repository.create(acc)
