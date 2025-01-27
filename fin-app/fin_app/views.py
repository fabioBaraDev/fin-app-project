
from rest_framework import viewsets

from fin_app.models import Aluno
from fin_app.serializer import AlunoSerializer


class AlunosViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
