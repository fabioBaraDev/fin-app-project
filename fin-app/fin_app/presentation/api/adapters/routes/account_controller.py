from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from fin_app.domain.services.account_service_interface import AccountServiceInterface
from fin_app.infrastructure.common.errors import AccountNotFoundError
from fin_app.presentation.api.adapters.serializers.account_serializer import (
    AccountSerializer,
)

# I used a curry from functional programming,
# in order to Django accept my dependency inversion strategy
from fin_app.presentation.api.adapters.util import is_valid_uuid


def account_controller(service: AccountServiceInterface):
    def get(request):
        accounts = service.get_all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def create(request):

        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            service.create(serializer.to_domain())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(["GET", "POST"])
    def base_path_route(request):
        if request.method == "GET":
            return get(request)

        if request.method == "POST":
            return create(request)

    @api_view(["GET"])
    def get_by_id(request, id):
        if not is_valid_uuid(id):
            return Response(
                {"error": "Invalid UUID format"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            account = service.get_by_id(id)
            serializer = AccountSerializer(account)
            return Response(serializer.data)
        except AccountNotFoundError as e:
            return Response({"error": e.message}, status=e.error_status)
        except:
            return Response(
                {"error": "internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return base_path_route, get_by_id
