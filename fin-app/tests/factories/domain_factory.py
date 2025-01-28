from datetime import datetime
from decimal import Decimal

from faker import Faker

from fin_app.domain.entities import AccountCategoryDomain, AccountDomain

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
