# Generated by Django 3.2 on 2021-05-12 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('immigration', '0020_auto_20210512_1251'),
    ]

    operations = [
        migrations.DeleteModel(
            name='IssuedDocumentType',
        ),
        migrations.RemoveField(
            model_name='issueddocument',
            name='process_step',
        ),
    ]
