# Generated by Django 3.2 on 2021-05-24 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("immigration", "0033_auto_20210521_1958"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="processstep",
            name="is_primary",
        ),
    ]
