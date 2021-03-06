# Generated by Django 3.2 on 2021-05-26 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0007_country_is_active"),
        ("immigration", "0035_auto_20210526_1904"),
    ]

    operations = [
        migrations.AlterField(
            model_name="processstep",
            name="estimated_max_duration_days",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Maximum number of working days this step is expected to take",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="processstep",
            name="estimated_min_duration_days",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Minimum number of working days this step is expected to take",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="processstep",
            name="host_country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="app.country",
            ),
        ),
    ]
