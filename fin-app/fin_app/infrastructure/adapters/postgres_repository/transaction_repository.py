from datetime import datetime
from decimal import Decimal
from typing import List

from fin_app.domain.entities import TransferDomain, AccountDomain
from fin_app.domain.ports.repository import TransactionRepositoryInterface
from fin_app.infrastructure.adapters.postgres_repository.mappers import TransferGetAllMapper, TransferMapper, \
    TransferFromListMapper
from fin_app.infrastructure.adapters.postgres_repository.models import Transaction, Account, Transfer


class TransactionRepository(TransactionRepositoryInterface):
    def get_all(self) -> list[TransferDomain]:
        transfers = Transfer.objects.prefetch_related('transfers__account').all()
        domains = []
        for transfer in transfers:
            domains.append(TransferGetAllMapper.to_entity(transfer))
        return domains

    def get_by_account_id(self, id, account: AccountDomain) -> List[TransferDomain]:
        transaction_transfer = []
        transactions = Transaction.objects.select_related('transfer').filter(account_id=id).all()
        for tr in transactions:
            transaction_transfer.append(
                TransferMapper.to_entity(
                    transfer=tr.transfer,
                    transaction=tr
                )
            )
        return transaction_transfer

    def transfer(self, transfer_domain: TransferDomain) -> TransferDomain:
        transfer = Transfer(
            id=transfer_domain.id,
            value=transfer_domain.value
        )

        transaction_from = Transaction(
            id=transfer_domain.money_from.id,
            value=transfer_domain.value,
            type=transfer_domain.money_from.type.value,
            created_at=transfer_domain.money_from.created_at,
            account_id=transfer_domain.money_from.account.id,
            transfer_id=transfer_domain.id
        )

        transaction_to = Transaction(
            id=transfer_domain.money_to.id,
            value=transfer_domain.value,
            type=transfer_domain.money_to.type.value,
            created_at=transfer_domain.money_to.created_at,
            account_id=transfer_domain.money_to.account.id,
            transfer_id=transfer_domain.id
        )

        transfer.save()
        transaction_to.save()
        transaction_from.save()

        Account.objects.filter(id=transfer_domain.money_from.account.id).update(
            balance=transfer_domain.money_from.account.balance)

        Account.objects.filter(id=transfer_domain.money_to.account.id).update(
            balance=transfer_domain.money_to.account.balance)

        return transfer_domain

    def get_by_transfer_id(self, id: Decimal) -> TransferDomain:
        transactions = Transaction.objects.select_related('transfer').filter(transfer_id=id).all()

        return TransferFromListMapper.to_entity(transactions)

    def cancel_transfer(self, transfer_domain: TransferDomain):
        Account.objects.filter(id=transfer_domain.money_from.account.id).update(
            balance=transfer_domain.money_from.account.balance)

        Account.objects.filter(id=transfer_domain.money_to.account.id).update(
            balance=transfer_domain.money_to.account.balance)

        Transfer.objects.filter(id=transfer_domain.id).update(
            cancel_at=datetime.now()
        )

        Transaction.objects.filter(id=transfer_domain.money_from.id).update(
            cancel_at=datetime.now()
        )

        Transaction.objects.filter(id=transfer_domain.money_to.id).update(
            cancel_at=datetime.now()
        )

