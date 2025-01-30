# Generated by Django 5.1.5 on 2025-01-29 18:16

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField()),
                (
                    "type",
                    models.CharField(
                        choices=[("A", "A"), ("B", "B"), ("C", "C")], max_length=1
                    ),
                ),
                (
                    "balance",
                    models.DecimalField(decimal_places=2, default=0, max_digits=100),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name="Transfer",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("value", models.DecimalField(decimal_places=2, max_digits=100)),
                (
                    "cancel_at",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("value", models.DecimalField(decimal_places=2, max_digits=100)),
                (
                    "type",
                    models.CharField(
                        choices=[("CASH_OUT", "CASH_OUT"), ("CASH_IN", "CASH_IN")],
                        max_length=8,
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to="fin_app.account",
                    ),
                ),
                (
                    "transfer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transfers",
                        to="fin_app.transfer",
                    ),
                ),
            ],
        ),
    ]
