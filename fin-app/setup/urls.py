from django.urls import include, path

from fin_app.presentation.api.server_builder import RouteBuilder

builder = RouteBuilder()

acc_base_route, acc_get_by_id = builder.build_account_route()

urlpatterns = [
    path("account/", acc_base_route, name="account"),
    path("account/<str:id>/", acc_get_by_id, name="get_account_by_id"),
]

handler404 = builder.custom_404_view
handler500 = builder.custom_500_view
