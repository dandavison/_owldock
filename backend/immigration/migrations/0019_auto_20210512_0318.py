# Generated by Django 3.2 on 2021-05-12 03:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("immigration", "0018_populate_issueddocument_m2m"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="issueddocument",
            name="issued_document_type",
        ),
    ]
