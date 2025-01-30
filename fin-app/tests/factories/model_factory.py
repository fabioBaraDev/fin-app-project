from datetime import datetime
from decimal import Decimal

from faker import Faker

from fin_app.domain.entities import AccountDomain, AccountCategoryDomain
from fin_app.infrastructure.adapters.postgres_repository.models import (
    Account,
)

faker = Faker()


class ModelFactories:
    @staticmethod
    def create_account_domain(domain: AccountDomain = None):
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
