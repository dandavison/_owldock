# Generated by Django 3.2 on 2021-07-12 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_country_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='immigration_summary_status',
            field=models.CharField(choices=[('Not started', 'Not Started'), ('Draft', 'Draft'), ('Final', 'Final')], default='Not started', max_length=16),
        ),
        migrations.AlterField(
            model_name='country',
            name='immigration_summary',
            field=models.TextField(blank=True),
        ),
    ]