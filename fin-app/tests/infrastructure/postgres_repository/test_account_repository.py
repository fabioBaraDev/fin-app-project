import unittest
from unittest.mock import Mock, patch

from fin_app.infrastructure.adapters.postgres_repository.account_repository import (
    Account,
    AccountNotFoundError,
    AccountRepository,
)
from tests.factories.domain_factory import DomainFactories
from tests.factories.model_factory import ModelFactories


class TestAccountRepository(unittest.TestCase):
    def setUp(self):
        self.mock_account_model = Mock(spec=Account)
        self.patcher_model = patch(
            "fin_app.infrastructure.adapters.postgres_repository.account_repository.Account",
            self.mock_account_model,
        )
        self.patcher_model.start()
        self.repository = AccountRepository()

    def tearDown(self):
        self.patcher_model.stop()

    def test_get_all(self):
        expected_domains = [
            DomainFactories.create_account_domain(),
            DomainFactories.create_account_domain(),
        ]

        mock_account_data = [
            ModelFactories.create_account_model(expected_domains[0]),
            ModelFactories.create_account_model(expected_domains[1]),
        ]
        self.mock_account_model.objects.all.return_value = mock_account_data

        result = self.repository.get_all()

        self.mock_account_model.objects.all.assert_called_once()
        self.assertEqual(result, expected_domains)

    def test_get_by_id_success(self):
        domain = DomainFactories.create_account_domain()
        self.mock_account_model.objects.get.return_value = (
            ModelFactories.create_account_model(domain)
        )

        result = self.repository.get_by_id(domain.id)

        self.mock_account_model.objects.get.assert_called_once_with(id=domain.id)
        self.assertEqual(result, domain)

    def test_get_by_id_not_found(self):
        domain = DomainFactories.create_account_domain()
        self.mock_account_model.objects.get.side_effect = Account.DoesNotExist

        with self.assertRaises(AccountNotFoundError):
            self.repository.get_by_id(domain.id)

        self.mock_account_model.objects.get.assert_called_once_with(id=domain.id)
