# Generated by Django 3.2 on 2021-06-02 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20210506_1802'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='casestep',
            options={},
        ),
        migrations.RemoveField(
            model_name='casestep',
            name='sequence_number',
        ),
    ]
