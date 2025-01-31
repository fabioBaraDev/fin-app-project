from unittest.mock import MagicMock
from uuid import uuid4

from django.test import RequestFactory, TestCase
from rest_framework import status

from fin_app.domain.errors import AccountNotFoundError
from fin_app.domain.services.transaction_service_interface import TransactionServiceInterface
from fin_app.presentation.api.adapters.routes.transaction_controller import transaction_controller
from fin_app.presentation.api.adapters.serializers.transaction_serializer import TransferByAccountSerializer
from test.factories.domain_factory import DomainFactories


class TestAccountController(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.service_mock = MagicMock(spec=TransactionServiceInterface)
        self.base_path_route, self.get_transaction_by_account_id, self.cancel_transfer = transaction_controller(
            service=self.service_mock
        )

    def test_should_get_transfers(self, ):
        request = self.factory.get("/transaction/")

        expected_domain = DomainFactories.create_transfer_domain()
        self.service_mock.get_all.return_value = [expected_domain]
        response = self.base_path_route(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([TransferByAccountSerializer(expected_domain).data], response.data['data'])
        self.service_mock.get_all.assert_called_once()

    def test_should_create_transfer(self):
        request = self.factory.post(
            "/transaction/",
            {'from_account_id': str(uuid4()), 'to_account_id': str(uuid4()), 'value': 100},
            content_type="application/json",
        )

        self.service_mock.create.return_value = None
        response = self.base_path_route(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Transfer executed successfully")

    def test_should_return_id_error_on_transfer(self):
        request = self.factory.post(
            "/transaction/",
            {'from_account_id': 'qququuq', 'to_account_id': str(uuid4()), 'value': 100},
            content_type="application/json",
        )

        self.service_mock.create.return_value = None
        response = self.base_path_route(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_return_value_error_on_transfer(self):
        request = self.factory.post(
            "/transaction/",
            {'from_account_id': str(uuid4()), 'to_account_id': str(uuid4())},
            content_type="application/json",
        )

        self.service_mock.create.return_value = None
        response = self.base_path_route(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_return_account_not_found_on_transfer(self):
        request = self.factory.post(
            "/transaction/",
            {'from_account_id': str(uuid4()), 'to_account_id': str(uuid4()), 'value': 100},
            content_type="application/json",
        )

        self.service_mock.create.side_effect = AccountNotFoundError(type='test')
        response = self.base_path_route(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_should_cancel_transfer(self):
        request = self.factory.post(
            "/transaction/cancel/",
            {'transfer_id': str(uuid4())},
            content_type="application/json",
        )

        self.service_mock.cancel_by_transfer_id.return_value = None
        response = self.cancel_transfer(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Cancel executed successfully")

    def test_should_return_invalid_data_on_cancel_transfer(self):
        request = self.factory.post(
            "/transaction/cancel/",
            {'transfer_id': 'hsudhsujdh11'},
            content_type="application/json",
        )

        self.service_mock.cancel_by_transfer_id.return_value = None
        response = self.cancel_transfer(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_get_transaction_by_account_id(self):
        id = "123e4567-e89b-12d3-a456-426614174000"
        request = self.factory.get(f"/transaction/{id}/")
        expected_domain = [DomainFactories.create_transfer_domain()]
        self.service_mock.get_by_account_id.return_value = expected_domain

        response = self.get_transaction_by_account_id(request, id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([TransferByAccountSerializer(expected_domain[0]).data], response.data['data'])
