from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from faker import Faker

from fin_app.domain.entities import (
    AccountCategoryDomain,
    AccountDomain,
    TransactionDomain,
    TransactionTypeDomain,
    TransferDomain,
)

faker = Faker()


class DomainFactories:
    @staticmethod
    def create_account_domain(name=None, type=None, id=None, balance=None):
        return AccountDomain(
            name=name if name else faker.text(max_nb_chars=50),
            type=type if type else faker.random_element(elements=AccountCategoryDomain),
            id=id if id else faker.uuid4(),
            balance=balance if balance else Decimal(faker.pyfloat()),
            created_at=str(datetime.now()),
        )

    @staticmethod
    def create_transaction_domain(type=None, acc=None):
        return TransactionDomain(
            value=Decimal(faker.pyfloat()),
            type=type if type else faker.random_element(elements=TransactionTypeDomain),
            account=acc if acc else DomainFactories.create_account_domain(balance=1000),
            created_at=datetime.now(),
            cancel_at=None,
            id=uuid4(),
        )

    @staticmethod
    def create_transfer_domain(value):
        return TransferDomain(
            value=Decimal(value if value else faker.pyfloat()),
            money_from=DomainFactories.create_transaction_domain(),
            money_to=DomainFactories.create_transaction_domain(),
            created_at=str(datetime.now()),
            id=uuid4(),
        )
