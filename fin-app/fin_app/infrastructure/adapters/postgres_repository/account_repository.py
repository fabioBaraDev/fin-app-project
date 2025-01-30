from typing import List

from django.core.exceptions import ObjectDoesNotExist

from fin_app.domain.entities import AccountDomain
from fin_app.domain.errors import AccountNotFoundError
from fin_app.domain.ports.repository import AccountRepositoryInterface
from fin_app.infrastructure.adapters.postgres_repository.mappers import AccountMapper
from fin_app.infrastructure.adapters.postgres_repository.models import Account


class AccountRepository(AccountRepositoryInterface):
    def get_all(self) -> List[AccountDomain]:
        return [AccountMapper.to_entity(row) for row in Account.objects.all()]

    def get_by_id(self, id) -> AccountDomain:
        try:
            response = Account.objects.get(id=id)
        except ObjectDoesNotExist:
            raise AccountNotFoundError(type=__name__)

        return AccountMapper.to_entity(response)

    def create(self, acc: AccountDomain) -> AccountDomain:
        instance = Account(id=acc.id, name=acc.name, type=acc.type, balance=acc.balance)
        instance.save()
        return acc
