from abc import ABC
from decimal import Decimal
from typing import List

from fin_app.domain.entities import AccountDomain, TransferDomain


class AccountRepositoryInterface(ABC):
    def get_all(self) -> List[AccountDomain]:
        pass

    def get_by_id(self, id) -> AccountDomain:
        pass

    def create(self, acc: AccountDomain) -> AccountDomain:
        pass


class TransactionRepositoryInterface(ABC):
    def get_all(self) -> List[TransferDomain]:
        pass

    def get_by_account_id(self, id, account: AccountDomain) -> List[TransferDomain]:
        pass

    def transfer(self, transfer: TransferDomain) -> TransferDomain:
        pass

    def cancel_transfer(self, transfer_domain: TransferDomain):
        pass

    def get_by_transfer_id(self, id: Decimal) -> TransferDomain:
        pass
