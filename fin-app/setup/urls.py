from django.urls import path

from fin_app.presentation.api.server_builder import RouteBuilder

builder = RouteBuilder()

acc_base_route, acc_get_by_id = builder.build_account_route()
transaction_base_route, get_transaction_by_account_id, cancel_transfer = (
    builder.build_transaction_route()
)

urlpatterns = [
    path("account/", acc_base_route, name="account"),
    path("account/<str:id>/", acc_get_by_id, name="get_account_by_id"),
    path("transaction/cancel/", cancel_transfer, name="cancel_transaction"),
    path("transaction/", transaction_base_route, name="transaction"),
    path("transaction/<str:id>/", get_transaction_by_account_id, name="transaction"),
]

handler404 = builder.custom_404_view
handler500 = builder.custom_500_view
