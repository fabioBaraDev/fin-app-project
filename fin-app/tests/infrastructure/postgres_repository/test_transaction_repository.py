import unittest
from unittest.mock import patch

import pytest

from fin_app.domain.entities import TransferDomain
from fin_app.infrastructure.adapters.postgres_repository.transaction_repository import (
    TransactionRepository,
)
from tests.factories.model_factory import ModelFactories


class TestTransactionRepository(unittest.TestCase):
    def setUp(self):
        self.repository = TransactionRepository()

    @pytest.mark.usefixtures("db")
    @patch(
        "fin_app.infrastructure.adapters.postgres_repository.models.Transfer.objects.prefetch_related"
    )
    def test_should_get_all_transfers(self, mock_prefetch_related):
        mock_prefetch_related.return_value.all.return_value = [
            ModelFactories.create_transfer_model()
        ]

        result = self.repository.get_all()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], TransferDomain)
        mock_prefetch_related.assert_called_once_with("transfers__account")
