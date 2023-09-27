# Generated by Django 4.2.5 on 2023-09-23 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [("customers", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("robot_serial", models.CharField(max_length=5)),
                ("customer", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="customers.customer")),
            ],
        )
    ]
