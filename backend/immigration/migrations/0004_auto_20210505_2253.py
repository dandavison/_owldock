# Generated by Django 3.2 on 2021-05-05 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('immigration', '0003_serviceitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processstep',
            name='estimated_max_duration_days',
            field=models.PositiveIntegerField(help_text='Maximum number of working days this step is expected to take', null=True),
        ),
        migrations.AlterField(
            model_name='processstep',
            name='estimated_min_duration_days',
            field=models.PositiveIntegerField(help_text='Minimum number of working days this step is expected to take', null=True),
        ),
    ]
