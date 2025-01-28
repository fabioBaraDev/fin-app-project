import unittest
from unittest.mock import Mock

from fin_app.application.account_service import (
    AccountRepositoryInterface,
    AccountService,
)
from tests.factories.domain_factory import DomainFactories


class TestAccountService(unittest.TestCase):
    def setUp(self):
        self.mock_repository = Mock(spec=AccountRepositoryInterface)
        self.account_service = AccountService(self.mock_repository)

    def test_get_all(self):
        expected_accounts = [
            DomainFactories.create_account_domain(),
            DomainFactories.create_account_domain(),
        ]
        self.mock_repository.get_all.return_value = expected_accounts

        result = self.account_service.get_all()

        self.mock_repository.get_all.assert_called_once()
        self.assertEqual(result, expected_accounts)

    def test_get_by_id(self):
        account_id = 1
        expected_account = DomainFactories.create_account_domain()
        self.mock_repository.get_by_id.return_value = expected_account

        result = self.account_service.get_by_id(account_id)

        self.mock_repository.get_by_id.assert_called_once_with(account_id)
        self.assertEqual(result, expected_account)

    def test_create(self):
        new_account = DomainFactories.create_account_domain()
        self.mock_repository.create.return_value = new_account

        result = self.account_service.create(new_account)

        self.mock_repository.create.assert_called_once_with(new_account)
        self.assertEqual(result, new_account)
