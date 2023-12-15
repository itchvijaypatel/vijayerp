# Generated by Django 5.0 on 2023-12-15 17:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0005_erp_plan_delete_role"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="erp_plan",
            name="price",
        ),
        migrations.AddField(
            model_name="erp_plan",
            name="monthly_price",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="erp_plan",
            name="yearly_price",
            field=models.FloatField(default=0.0),
        ),
    ]