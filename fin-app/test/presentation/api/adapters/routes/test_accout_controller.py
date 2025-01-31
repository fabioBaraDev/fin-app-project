from unittest.mock import MagicMock

from django.test import RequestFactory, TestCase
from rest_framework import status

from fin_app.domain.errors import AccountNotFoundError
from fin_app.domain.services.account_service_interface import AccountServiceInterface
from fin_app.presentation.api.adapters.routes.account_controller import (
    account_controller,
)
from test.factories.domain_factory import DomainFactories


class TestAccountController(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.service_mock = MagicMock(spec=AccountServiceInterface)
        self.base_path_route, self.get_by_id = account_controller(
            service=self.service_mock
        )

    def test_should_get_all_accounts(self):
        request = self.factory.get("/accounts/")
        self.service_mock.get_all.return_value = []

        response = self.base_path_route(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.service_mock.get_all.assert_called_once()

    def test_should_create_account(self):
        request = self.factory.post(
            "/accounts/",
            {"name": "Test Account", "type": "A", "balance": 1000},
            content_type="application/json",
        )

        expected_account = DomainFactories.create_account_domain()
        self.service_mock.create.return_value = expected_account

        response = self.base_path_route(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {
                "id": str(expected_account.id),
                "name": expected_account.name,
                "type": expected_account.type.value,
                "balance": str(round(expected_account.balance, 2)),
            },
        )
        self.service_mock.create.assert_called_once()

    def test_should_get_account_by_id_with_valid_id(self):
        account_id = "123e4567-e89b-12d3-a456-426614174000"
        request = self.factory.get(f"/accounts/{account_id}/")
        expected_domain = DomainFactories.create_account_domain(id=account_id)
        self.service_mock.get_by_id.return_value = expected_domain

        response = self.get_by_id(request, account_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.service_mock.get_by_id.assert_called_once_with(account_id)
        self.assertEqual(
            response.data,
            {
                "id": expected_domain.id,
                "name": expected_domain.name,
                "type": expected_domain.type.name,
                "balance": str(round(expected_domain.balance, 2)),
            },
        )

    def test_should_get_erorr_with_invalid_id(self):
        invalid_account_id = "invalid-uuid"
        request = self.factory.get(f"/accounts/{invalid_account_id}/")

        response = self.get_by_id(request, invalid_account_id)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Invalid UUID format"})

    def test_should_get_not_found_error(self):
        account_id = "123e4567-e89b-12d3-a456-426614174000"
        request = self.factory.get(f"/accounts/{account_id}/")
        self.service_mock.get_by_id.side_effect = AccountNotFoundError(type=__name__)

        response = self.get_by_id(request, account_id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "account not found error"})

    def test_should_get_internal_server_error(self):
        account_id = "123e4567-e89b-12d3-a456-426614174000"
        request = self.factory.get(f"/accounts/{account_id}/")
        self.service_mock.get_by_id.side_effect = Exception("Internal server error")

        response = self.get_by_id(request, account_id)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data, {"error": "internal server error"})
