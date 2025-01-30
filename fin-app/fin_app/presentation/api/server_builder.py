from django.http import JsonResponse

from fin_app.application.account_service import AccountService
from fin_app.application.transaction_service import TransactionService
from fin_app.infrastructure.adapters.postgres_repository.account_repository import (
    AccountRepository,
)
from fin_app.infrastructure.adapters.postgres_repository.transaction_repository import TransactionRepository
from fin_app.presentation.api.adapters.routes.account_controller import (
    account_controller,
)
from fin_app.presentation.api.adapters.routes.transaction_controller import transaction_controller


class RouteBuilder:
    @classmethod
    def build_account_route(cls):
        repository = AccountRepository()
        service = AccountService(repository)
        return account_controller(service)

    @classmethod
    def build_transaction_route(cls):
        repository = TransactionRepository()
        account_repository = AccountRepository()
        service = TransactionService(repository, account_repository)
        return transaction_controller(service)

    @staticmethod
    def custom_404_view(request, exception=None):
        return JsonResponse(
            {"error": "The requested resource was not found."}, status=404
        )

    @staticmethod
    def custom_500_view(request, exception=None):
        return JsonResponse({"error": "Internal Server Error"}, status=500)
