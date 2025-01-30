import unittest
from decimal import Decimal

from fin_app.domain.entities import (
    AccountCategoryDomain,
    AccountDomain,
    FromAccountHasNoFundsToTransfer,
    FromAccountHasNoMoneyToTransfer,
    TransactionTypeDomain,
    TransferDomain,
)


class TestTransferDomain(unittest.TestCase):
    def setUp(self):
        self.from_account = AccountDomain(
            name="John Doe", type=AccountCategoryDomain.A, balance=Decimal("1000.00")
        )
        self.to_account = AccountDomain(
            name="Jane Doe", type=AccountCategoryDomain.B, balance=Decimal("500.00")
        )
        self.transfer = TransferDomain.build_transfer(
            from_account=self.from_account,
            to_account=self.to_account,
            value=Decimal("200.00"),
        )

    def test_transfer(self):
        self.transfer.transfer()
        self.assertEqual(self.from_account.balance, Decimal("800.00"))
        self.assertEqual(self.to_account.balance, Decimal("700.00"))
        self.assertEqual(self.transfer.money_from.type, TransactionTypeDomain.CASH_OUT)
        self.assertEqual(self.transfer.money_to.type, TransactionTypeDomain.CASH_IN)

    def test_transfer_no_money(self):
        self.from_account.deduct_balance(Decimal("1000.00"))
        with self.assertRaises(FromAccountHasNoMoneyToTransfer):
            self.transfer.transfer()

    def test_transfer_no_funds(self):
        with self.assertRaises(FromAccountHasNoFundsToTransfer):
            self.transfer.value = Decimal("1500.00")
            self.transfer.transfer()

    def test_cancel(self):
        self.transfer.transfer()
        self.transfer.cancel()
        self.assertEqual(self.from_account.balance, Decimal("1000.00"))
        self.assertEqual(self.to_account.balance, Decimal("500.00"))
        self.assertIsNotNone(self.transfer.cancel_at)
        self.assertIsNotNone(self.transfer.money_from.cancel_at)
        self.assertIsNotNone(self.transfer.money_to.cancel_at)

    def test_build_transfer(self):
        transfer = TransferDomain.build_transfer(
            from_account=self.from_account,
            to_account=self.to_account,
            value=Decimal("200.00"),
        )
        self.assertEqual(transfer.value, Decimal("200.00"))
        self.assertEqual(transfer.money_from.account, self.from_account)
        self.assertEqual(transfer.money_to.account, self.to_account)
