# Generated by Django 3.2 on 2021-05-09 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('immigration', '0012_auto_20210509_0120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processstep',
            name='process_ruleset',
        ),
    ]
