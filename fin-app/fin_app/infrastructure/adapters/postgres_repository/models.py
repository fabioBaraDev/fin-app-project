import uuid
from enum import Enum

from django.db import models
from django.utils import timezone


class AccountCategory(Enum):
    A = "A"
    B = "B"
    C = "C"


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField()
    type = models.CharField(
        max_length=1,
        choices=(
            (AccountCategory.A.name, AccountCategory.A.value),
            (AccountCategory.B.name, AccountCategory.B.value),
            (AccountCategory.C.name, AccountCategory.C.value),
        ),
    )
    balance = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.DecimalField(max_digits=100, decimal_places=2)
    cancel_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transactions"
    )

    def __str__(self):
        return self.id
