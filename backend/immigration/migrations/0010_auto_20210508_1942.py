# Generated by Django 3.2 on 2021-05-08 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('immigration', '0009_alter_processstep_host_country'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='processstep',
            options={},
        ),
        migrations.RemoveField(
            model_name='processstep',
            name='sequence_number',
        ),
    ]
