# Generated by Django 4.2 on 2023-04-14 20:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="zip_code",
            field=models.CharField(
                default="00000",
                max_length=10,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Invalid ZIP Code", regex="^[0-9]{5}(?:-[0-9]{4})?$"
                    )
                ],
            ),
        ),
    ]
