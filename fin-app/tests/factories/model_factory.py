import uuid
from datetime import datetime
from decimal import Decimal

import pytest
from faker import Faker

from fin_app.domain.entities import (
    AccountCategoryDomain,
    AccountDomain,
    TransactionTypeDomain,
    TransferDomain,
)
from fin_app.infrastructure.adapters.postgres_repository.models import (
    Account,
    Transaction,
    Transfer,
)

faker = Faker()


class ModelFactories:
    @staticmethod
    def create_account_model(domain: AccountDomain = None):
        return Account(
            name=domain.name if domain else faker.text(max_nb_chars=50),
            type=(
                domain.type
                if domain
                else faker.random_element(elements=AccountCategoryDomain)
            ),
            id=domain.id if domain else faker.uuid4(),
            balance=domain.balance if domain.balance else Decimal(faker.pyfloat()),
            created_at=domain.created_at if domain.created_at else str(datetime.now()),
        )

    @staticmethod
    def create_transfer_model(domain: TransferDomain = None) -> Transfer:
        return Transfer(
            id=domain.id if domain else uuid.uuid4(),
            value=(
                domain.value
                if domain
                else Decimal(
                    faker.pydecimal(left_digits=5, right_digits=2, positive=True)
                )
            ),
            cancel_at=domain.cancel_at if domain else None,
            created_at=domain.created_at if domain else datetime.now(),
        )

    @staticmethod
    def create_transaction_model(domain: TransactionTypeDomain = None) -> Transaction:
        return Transaction(
            id=domain.id if domain else uuid.uuid4(),
            value=(
                domain.value
                if domain
                else Decimal(
                    faker.pydecimal(left_digits=5, right_digits=2, positive=True)
                )
            ),
            type=(
                domain.type
                if domain
                else faker.random_element(
                    elements=[
                        TransactionTypeDomain.CASH_OUT.name,
                        TransactionTypeDomain.CASH_IN.name,
                    ]
                )
            ),
            created_at=domain.created_at if domain else datetime.now(),
            cancel_at=domain.cancel_at if domain else None,
            account=domain.account if domain else None,
            transfer=domain.transfer if domain else None,
        )
