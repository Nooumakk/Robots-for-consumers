# Generated by Django 4.2.5 on 2023-09-28 16:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("orders", "0002_order_is_active")]

    operations = [migrations.AlterField(model_name="order", name="is_active", field=models.BooleanField(default=True))]
