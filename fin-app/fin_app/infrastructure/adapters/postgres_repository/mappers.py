from typing import List

from fin_app.domain.entities import (
    AccountDomain,
    TransactionDomain,
    TransactionTypeDomain,
    TransferDomain,
)
from fin_app.domain.errors import TransactionTypeMismatchError
from fin_app.infrastructure.adapters.postgres_repository.models import (
    Transaction,
    Transfer,
)


class AccountMapper:
    @classmethod
    def to_entity(cls, data):
        return AccountDomain(
            id=data.id,
            name=data.name,
            type=data.type,
            balance=data.balance,
            created_at=data.created_at,
        )


class TransferGetAllMapper:
    @classmethod
    def to_entity(cls, transfer: Transfer):
        transfer_domain = TransferDomain(
            id=transfer.id,
            value=transfer.value,
            created_at=transfer.created_at,
            cancel_at=transfer.cancel_at,
        )
        transactions = transfer.transfers.all()
        for transaction in transactions:
            if transaction.type == TransactionTypeDomain.CASH_IN.value:
                transfer_domain.money_to = TransactionMapper.to_entity(transaction)
            else:
                transfer_domain.money_from = TransactionMapper.to_entity(transaction)
        return transfer_domain


class TransactionMapper:
    @classmethod
    def to_entity(cls, transaction: Transaction):
        return TransactionDomain(
            id=transaction.id,
            value=transaction.value,
            type=transaction.type,
            account=AccountMapper.to_entity(transaction.account),
            created_at=transaction.created_at,
            cancel_at=transaction.cancel_at,
        )


class TransferMapper:
    @classmethod
    def to_entity(cls, transfer: Transfer, transaction: Transaction):
        transfer_domain = TransferDomain(
            id=transfer.id,
            value=transfer.value,
            created_at=transfer.created_at,
            cancel_at=transfer.cancel_at,
        )

        if transaction.type == TransactionTypeDomain.CASH_IN.value:
            transfer_domain.money_to = TransactionMapper.to_entity(transaction)
        else:
            transfer_domain.money_from = TransactionMapper.to_entity(transaction)

        return transfer_domain


class TransferFromListMapper:
    @classmethod
    def to_entity(cls, transaction: List[Transaction]):
        money_to, money_from = None, None
        for trans in transaction:
            if trans.type == TransactionTypeDomain.CASH_IN.value:
                money_to = TransactionMapper.to_entity(trans)
            elif trans.type == TransactionTypeDomain.CASH_OUT.value:
                money_from = TransactionMapper.to_entity(trans)

        if money_to is None or money_from is None:
            raise TransactionTypeMismatchError(type=__name__)

        transfer_domain = TransferDomain(
            id=transaction[0].transfer.id,
            value=transaction[0].transfer.value,
            created_at=transaction[0].transfer.created_at,
            money_to=money_to,
            money_from=money_from,
            cancel_at=transaction[0].cancel_at,
        )

        return transfer_domain
