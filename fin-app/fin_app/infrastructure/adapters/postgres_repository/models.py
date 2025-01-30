import uuid

from django.db import models
from django.utils import timezone

from fin_app.domain.entities import AccountCategoryDomain, TransactionTypeDomain


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField()
    type = models.CharField(
        max_length=1,
        choices=(
            (AccountCategoryDomain.A.name, AccountCategoryDomain.A.value),
            (AccountCategoryDomain.B.name, AccountCategoryDomain.B.value),
            (AccountCategoryDomain.C.name, AccountCategoryDomain.C.value),
        ),
    )
    balance = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Transfer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.DecimalField(max_digits=100, decimal_places=2)
    cancel_at = models.DateTimeField(default=None, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.DecimalField(max_digits=100, decimal_places=2)
    type = models.CharField(
        max_length=8,
        choices=(
            (TransactionTypeDomain.CASH_OUT.name, TransactionTypeDomain.CASH_OUT.value),
            (TransactionTypeDomain.CASH_IN.name, TransactionTypeDomain.CASH_IN.value),
        ),
    )
    created_at = models.DateTimeField(default=timezone.now)
    cancel_at = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transactions"
    )

    transfer = models.ForeignKey(
        Transfer, on_delete=models.CASCADE, related_name="transfers"
    )

