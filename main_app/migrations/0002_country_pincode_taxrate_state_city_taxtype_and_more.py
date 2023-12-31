# Generated by Django 5.0 on 2023-12-12 09:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("country", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "flag",
                    models.ImageField(blank=True, null=True, upload_to="country_flag"),
                ),
                ("status", models.IntegerField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Pincode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("city_name", models.CharField(blank=True, max_length=200, null=True)),
                ("pincode", models.CharField(blank=True, max_length=200, null=True)),
                ("status", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="TaxRate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rate", models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="State",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("state", models.CharField(blank=True, max_length=255, null=True)),
                ("status", models.IntegerField(default=True)),
                (
                    "country",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main_app.country",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("city", models.CharField(blank=True, max_length=255, null=True)),
                ("status", models.IntegerField(default=True)),
                (
                    "state",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main_app.state",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TaxType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=50, null=True)),
                ("rate", models.ManyToManyField(blank=True, to="main_app.taxrate")),
            ],
        ),
        migrations.CreateModel(
            name="TaxCurrencySymbol",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tax_name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "currency_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("symbol", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "country",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main_app.country",
                    ),
                ),
                (
                    "tax_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main_app.taxtype",
                    ),
                ),
            ],
        ),
    ]
