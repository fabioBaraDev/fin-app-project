import uuid

from rest_framework import serializers

from fin_app.domain.entities import AccountCategoryDomain, AccountDomain


class AccountSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    type = serializers.ChoiceField(
        choices=(
            (AccountCategoryDomain.A.name, AccountCategoryDomain.A.value),
            (AccountCategoryDomain.B.name, AccountCategoryDomain.B.value),
            (AccountCategoryDomain.C.name, AccountCategoryDomain.C.value),
        )
    )
    balance = serializers.DecimalField(max_digits=100, decimal_places=2, default=0)

    def create(self, validated_data):
        return AccountDomain(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        return instance

    def to_domain(self):
        return AccountDomain(
            id=uuid.uuid4(),
            name=self.validated_data["name"],
            type=self.validated_data["type"],
            balance=self.validated_data["balance"],
        )
