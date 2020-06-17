# Generated by Django 3.0.6 on 2020-06-17 15:15
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="InvitedEmail",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("address", models.EmailField(max_length=254, unique=True)),
            ],
        ),
    ]
