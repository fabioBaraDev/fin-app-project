import unittest
from decimal import Decimal
from unittest.mock import Mock
from uuid import uuid4

from fin_app.application.transaction_service import TransactionService
from fin_app.domain.entities import AccountCategoryDomain, AccountDomain, TransferDomain
from fin_app.domain.errors import AccountNotFoundError, TransactionNotFoundError
from fin_app.presentation.api.adapters.serializers.transaction_serializer import (
    TransactTransferSerializer,
)
from tests.factories.domain_factory import DomainFactories


class TestTransactionService(unittest.TestCase):
    def setUp(self):
        self.mock_repository = Mock()
        self.mock_account_repository = Mock()
        self.service = TransactionService(
            self.mock_repository, self.mock_account_repository
        )

    def test_should_get_all_transfers(self):
        transfer_domain = TransferDomain(value=Decimal(100))
        self.mock_repository.get_all.return_value = [transfer_domain]

        result = self.service.get_all()
        self.assertEqual(result, [transfer_domain])
        self.mock_repository.get_all.assert_called_once()

    def test_should_get_by_account_id_with_success_return(self):
        account_id = uuid4()
        account = AccountDomain(
            name="John Doe", type=AccountCategoryDomain.A, balance=Decimal(1000)
        )
        transfer_domain = TransferDomain(value=Decimal(100))

        self.mock_account_repository.get_by_id.return_value = account
        self.mock_repository.get_by_account_id.return_value = [transfer_domain]

        result = self.service.get_by_account_id(account_id)
        self.assertEqual(result, [transfer_domain])
        self.mock_account_repository.get_by_id.assert_called_once_with(account_id)
        self.mock_repository.get_by_account_id.assert_called_once_with(
            account_id, account
        )

    def test_should_return_account_not_found_when_account_id_is_not_found(self):
        account_id = uuid4()

        self.mock_account_repository.get_by_id.return_value = None

        with self.assertRaises(AccountNotFoundError):
            self.service.get_by_account_id(account_id)

    def test_should_return_transaction_not_found(self):
        account_id = uuid4()
        account = AccountDomain(
            name="John Doe", type=AccountCategoryDomain.A, balance=Decimal(1000)
        )

        self.mock_account_repository.get_by_id.return_value = account
        self.mock_repository.get_by_account_id.return_value = []

        with self.assertRaises(TransactionNotFoundError):
            self.service.get_by_account_id(account_id)

    def test_should_create_transfer_successfully(self):
        from_account_id = uuid4()
        to_account_id = uuid4()
        from_account = AccountDomain(
            name="John Doe", type=AccountCategoryDomain.A, balance=Decimal(1000)
        )
        to_account = AccountDomain(
            name="Jane Doe", type=AccountCategoryDomain.B, balance=Decimal(500)
        )
        value = Decimal("100.0")

        self.mock_account_repository.get_by_id.side_effect = [from_account, to_account]
        self.mock_repository.transfer.return_value = TransferDomain(value=value)

        data = TransactTransferSerializer(
            {
                "from_account_id": from_account_id,
                "to_account_id": to_account_id,
                "value": value,
            }
        )

        result = self.service.create(data.data)
        self.assertIsInstance(result, TransferDomain)
        self.mock_account_repository.get_by_id.assert_any_call(str(from_account_id))
        self.mock_account_repository.get_by_id.assert_any_call(str(to_account_id))
        self.mock_repository.transfer.assert_called_once()

    def test_should_return_account_not_found_when_there_is_no_account_to_transact(self):
        from_account_id = uuid4()
        to_account_id = uuid4()

        self.mock_account_repository.get_by_id.return_value = None

        data = TransactTransferSerializer(
            {
                "from_account_id": from_account_id,
                "to_account_id": to_account_id,
                "value": Decimal("100.0"),
            }
        )

        with self.assertRaises(AccountNotFoundError):
            self.service.create(data)

    def test_should_cancel_transaction(self):
        transfer_id = uuid4()
        transfer_domain = DomainFactories.create_transfer_domain(100)

        self.mock_repository.get_by_transfer_id.return_value = transfer_domain

        self.service.cancel_by_transfer_id(transfer_id)

        self.mock_repository.get_by_transfer_id.assert_called_once_with(transfer_id)
        self.mock_repository.cancel_transfer.assert_called_once_with(transfer_domain)
