import uuid
from decimal import Decimal
from typing import List

from django.core.exceptions import ObjectDoesNotExist

from fin_app.domain.entities import TransferDomain
from fin_app.domain.errors import AccountNotFoundError, TransactionNotFoundError
from fin_app.domain.ports.repository import (
    AccountRepositoryInterface,
    TransactionRepositoryInterface,
)
from fin_app.domain.services.transaction_service_interface import (
    TransactionServiceInterface,
)
from fin_app.presentation.api.adapters.serializers.transaction_serializer import (
    TransactTransferSerializer,
)


class TransactionService(TransactionServiceInterface):
    def __init__(
        self,
        repository: TransactionRepositoryInterface,
        account_repository: AccountRepositoryInterface,
    ):
        self.repository = repository
        self.account_repository = account_repository

    def get_all(self) -> List[TransferDomain]:
        return self.repository.get_all()

    def get_by_account_id(self, id: uuid.UUID) -> List[TransferDomain]:
        try:
            account = self.account_repository.get_by_id(id)
            if not account:
                raise AccountNotFoundError(type=__name__)

            transaction_transfer = self.repository.get_by_account_id(id, account)
            if not transaction_transfer:
                raise TransactionNotFoundError(type=__name__)

        except ObjectDoesNotExist:
            raise TransactionNotFoundError(type=__name__)

        return transaction_transfer

    def create(self, data: TransactTransferSerializer):
        from_account = self.account_repository.get_by_id(data["from_account_id"])
        to_account = self.account_repository.get_by_id(data["to_account_id"])

        if not (from_account and to_account):
            raise AccountNotFoundError(type=__name__)

        transfer = TransferDomain.build_transfer(
            from_account=from_account,
            to_account=to_account,
            value=Decimal(data["value"]),
        )
        transfer.transfer()

        return self.repository.transfer(transfer)

    def cancel_by_transfer_id(self, id: uuid.UUID):

        transfer_domain = self.repository.get_by_transfer_id(id)

        transfer_domain.cancel()
        self.repository.cancel_transfer(transfer_domain)
