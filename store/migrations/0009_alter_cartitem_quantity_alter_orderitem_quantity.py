# Generated by Django 4.2 on 2023-04-22 10:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0008_alter_cartitem_cart"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartitem",
            name="quantity",
            field=models.PositiveSmallIntegerField(
                validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="quantity",
            field=models.PositiveIntegerField(
                validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
    ]
