# Generated by Django 5.0 on 2023-12-15 17:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_app", "0002_erp_user_created_at_erp_user_updated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="erp_user",
            name="is_employee",
            field=models.BooleanField(default=False),
        ),
    ]