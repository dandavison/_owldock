# Generated by Django 3.2 on 2021-05-19 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_bloc_countries'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='immigration_summary',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]