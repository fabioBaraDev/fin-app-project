from django.urls import path, include
from rest_framework import routers

from fin_app.views import AlunosViewSet

router = routers.DefaultRouter()
router.register("alunos", AlunosViewSet, basename="Alunos")

urlpatterns = [path("", include(router.urls))]
