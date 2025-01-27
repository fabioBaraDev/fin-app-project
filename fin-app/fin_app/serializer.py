from fin_app.models import Aluno
from rest_framework import serializers


class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ["id", "nome", "rg", "cpf", "data_nascimento"]
