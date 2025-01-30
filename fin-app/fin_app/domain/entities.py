import enum
import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from fin_app.domain.errors import (
    FromAccountHasNoFundsToTransfer,
    FromAccountHasNoMoneyToTransfer,
)


class AccountCategoryDomain(enum.Enum):
    A = "A"
    B = "B"
    C = "C"


class TransactionTypeDomain(enum.Enum):
    CASH_IN = "CASH_IN"
    CASH_OUT = "CASH_OUT"


@dataclass
class AccountDomain:
    name: str
    type: AccountCategoryDomain
    id: uuid.UUID = uuid.uuid4()
    balance: Decimal = 0
    created_at: datetime = datetime.now()

    def deduct_balance(self, value: Decimal):
        self.balance -= value

    def add_to_balance(self, value: Decimal):
        self.balance += value

    def is_balance_positive(self):
        return self.balance > 0

    def has_funds(self, value: Decimal):
        return self.balance > value


@dataclass
class TransactionDomain:
    value: Decimal
    type: TransactionTypeDomain
    account: AccountDomain
    created_at: datetime = datetime.now()
    cancel_at: datetime = None
    id: uuid.UUID = uuid.uuid4()

    def deposit(self, value: Decimal):
        self.account.add_to_balance(value)

    def withdrawal(self, value: Decimal):
        if not self.account.is_balance_positive():
            raise FromAccountHasNoMoneyToTransfer(type=__name__)

        if not self.account.has_funds(value):
            raise FromAccountHasNoFundsToTransfer(type=__name__)

        self.account.deduct_balance(value)

    def cancel(self):
        self.cancel_at = datetime.now()


@dataclass
class TransferDomain:
    value: Decimal
    money_from: TransactionDomain = None
    money_to: TransactionDomain = None
    cancel_at: datetime = None
    created_at: datetime = datetime.now()
    id: uuid.UUID = uuid.uuid4()

    def transfer(self):
        self.money_from.withdrawal(value=self.value)
        self.money_from.type = TransactionTypeDomain.CASH_OUT

        self.money_to.deposit(value=self.value)
        self.money_to.type = TransactionTypeDomain.CASH_IN

    def cancel(self):
        self.cancel_at = datetime.now()
        self.money_from.deposit(value=self.value)
        self.money_from.cancel()
        self.money_to.withdrawal(value=self.value)
        self.money_to.cancel()

    @classmethod
    def build_transfer(
        cls, from_account: AccountDomain, to_account: AccountDomain, value: Decimal
    ):
        money_from = TransactionDomain(
            id=uuid.uuid4(),
            value=value,
            type=TransactionTypeDomain.CASH_OUT,
            account=from_account,
        )

        money_to = TransactionDomain(
            id=uuid.uuid4(),
            value=value,
            type=TransactionTypeDomain.CASH_IN,
            account=to_account,
        )

        return cls(
            id=uuid.uuid4(),
            value=value,
            money_from=money_from,
            money_to=money_to,
        )
