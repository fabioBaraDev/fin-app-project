from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from fin_app.domain.errors import (
    AccountNotFoundError,
    FromAccountHasNoFundsToTransfer,
    TransactionNotFoundError,
    TransactionTypeMismatchError,
)
from fin_app.domain.services.transaction_service_interface import (
    TransactionServiceInterface,
)
from fin_app.presentation.api.adapters.serializers.transaction_serializer import (
    CancelTransactSerializer,
    PageTransferSerializer,
    TransactTransferSerializer,
    TransferByAccountSerializer,
    TransferSerializer,
)
from fin_app.presentation.api.adapters.util import is_valid_uuid


# I used a curry from functional programming,
# in order to Django accept my dependency inversion strategy
def transaction_controller(service: TransactionServiceInterface):
    def get(request):
        transfers = service.get_all()

        page_number = request.GET.get("page", 1)
        paginator = Paginator(transfers, 3)
        page_obj = paginator.get_page(page_number)

        response = PageTransferSerializer(
            {
                "data": page_obj.object_list,
                "count": paginator.count,
                "num_pages": paginator.num_pages,
                "current_page": page_obj.number,
            }
        )

        return Response(response.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def create(request):
        try:
            serializer = TransactTransferSerializer(data=request.data)
            if serializer.is_valid():
                service.create(serializer.validated_data)
                return Response(
                    {"message": "Transfer executed successfully"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (
            FromAccountHasNoFundsToTransfer,
            AccountNotFoundError,
            TransactionNotFoundError,
        ) as e:
            return Response({"error": e.message}, status=e.error_status)
        except:
            return Response(
                {"error": "internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @transaction.atomic
    @api_view(["POST"])
    def cancel_transfer(request):
        try:
            serializer = CancelTransactSerializer(data=request.data)
            if serializer.is_valid():
                service.cancel_by_transfer_id(
                    serializer.validated_data.get("transfer_id")
                )
                return Response(
                    {"message": "Cancel executed successfully"},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TransactionTypeMismatchError as e:
            return Response({"error": e.message}, status=e.error_status)
        except:
            return Response(
                {"error": "internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @api_view(["GET", "POST"])
    def base_path_route(request):
        if request.method == "GET":
            return get(request)

        if request.method == "POST":
            return create(request)

    @api_view(["GET"])
    def get_transaction_by_account_id(request, id):
        if not is_valid_uuid(id):
            return Response(
                {"error": "Invalid UUID format"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            transfers = service.get_by_account_id(id)

            page_number = request.GET.get("page", 1)
            paginator = Paginator(transfers, 3)
            page_obj = paginator.get_page(page_number)

            response = PageTransferSerializer(
                {
                    "data": page_obj.object_list,
                    "count": paginator.count,
                    "num_pages": paginator.num_pages,
                    "current_page": page_obj.number,
                }
            )

            return Response(response.data, status=status.HTTP_200_OK)
        except (AccountNotFoundError, TransactionNotFoundError) as e:
            return Response({"error": e.message}, status=e.error_status)
        except Exception as e:
            return Response(
                {"error": "internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return base_path_route, get_transaction_by_account_id, cancel_transfer
