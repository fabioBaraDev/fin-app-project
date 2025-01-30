from rest_framework import serializers

from fin_app.domain.entities import TransactionTypeDomain, TransactionDomain, TransferDomain
from fin_app.presentation.api.adapters.serializers.account_serializer import AccountSerializer
from rest_framework.validators import ValidationError


class TransactionSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    value = serializers.DecimalField(max_digits=100, decimal_places=2)
    type = serializers.ChoiceField(
        choices=(
            (TransactionTypeDomain.CASH_IN.name, TransactionTypeDomain.CASH_IN.value),
            (TransactionTypeDomain.CASH_OUT.name, TransactionTypeDomain.CASH_OUT.value)
        )
    )
    account = AccountSerializer()
    created_at = serializers.DateTimeField()

    def create(self, validated_data):
        return TransactionDomain(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get("id", instance.id)
        return instance


class TransferSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    value = serializers.DecimalField(max_digits=100, decimal_places=2)
    money_from = TransactionSerializer()
    money_to = TransactionSerializer()
    cancel_at = serializers.DateTimeField(required=False)
    created_at = serializers.DateTimeField()

    def create(self, validated_data):
        return TransferDomain(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get("id", instance.id)
        return instance


class TransferByAccountSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    value = serializers.DecimalField(max_digits=100, decimal_places=2)
    details = serializers.SerializerMethodField()
    cancel_at = serializers.DateTimeField(required=False)
    created_at = serializers.DateTimeField()

    def get_details(self, obj):
        data = obj.money_from if obj.money_from else obj.money_to
        return TransactionSerializer(data).data

    def create(self, validated_data):
        return TransferDomain(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get("id", instance.id)
        return instance


class TransactTransferSerializer(serializers.Serializer):
    from_account_id = serializers.UUIDField()
    to_account_id = serializers.UUIDField()
    value = serializers.DecimalField(max_digits=100, decimal_places=2)

    def validate_value(self, value):
        if value <= 0:
            raise ValidationError("The transfer value must be greater than zero")
        return value

    def create(self, validated_data):
        self.from_account_id = validated_data['from_account_id']
        self.to_account_id = validated_data['to_account_id']
        self.value = validated_data['value']

    def update(self, instance, validated_data):
        pass


class CancelTransactSerializer(serializers.Serializer):
    transfer_id = serializers.UUIDField()

    def create(self, validated_data):
        self.transfer_id = validated_data['transfer_id']

    def update(self, instance, validated_data):
        pass


class PageTransferSerializer(serializers.Serializer):
    data = TransferByAccountSerializer(many=True)
    count = serializers.IntegerField()
    num_pages = serializers.IntegerField()
    current_page = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
