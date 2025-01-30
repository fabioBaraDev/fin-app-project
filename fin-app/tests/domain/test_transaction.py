import unittest
from decimal import Decimal

from fin_app.domain.entities import (
    AccountCategoryDomain,
    AccountDomain,
    FromAccountHasNoFundsToTransfer,
    FromAccountHasNoMoneyToTransfer,
    TransactionDomain,
    TransactionTypeDomain,
)


class TestTransactionDomain(unittest.TestCase):
    def setUp(self):
        self.account = AccountDomain(
            name="John Doe", type=AccountCategoryDomain.A, balance=Decimal("1000.00")
        )
        self.transaction = TransactionDomain(
            value=Decimal("100.00"),
            type=TransactionTypeDomain.CASH_OUT,
            account=self.account,
        )

    def test_deposit(self):
        self.transaction.deposit(Decimal("200.00"))
        self.assertEqual(self.account.balance, Decimal("1200.00"))

    def test_withdrawal_success(self):
        self.transaction.withdrawal(Decimal("100.00"))
        self.assertEqual(self.account.balance, Decimal("900.00"))

    def test_withdrawal_no_money(self):
        self.account.deduct_balance(Decimal("1000.00"))
        with self.assertRaises(FromAccountHasNoMoneyToTransfer):
            self.transaction.withdrawal(Decimal("100.00"))

    def test_withdrawal_no_funds(self):
        with self.assertRaises(FromAccountHasNoFundsToTransfer):
            self.transaction.withdrawal(Decimal("1500.00"))

    def test_cancel(self):
        self.transaction.cancel()
        self.assertIsNotNone(self.transaction.cancel_at)
