# Generated by Django 3.2 on 2021-05-15 15:07

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ("immigration", "0030_auto_20210513_1640"),
    ]

    operations = [
        migrations.AlterField(
            model_name="processruleset",
            name="minimum_salary",
            field=djmoney.models.fields.MoneyField(
                blank=True,
                decimal_places=2,
                default_currency="EUR",
                help_text="Monthly gross amount; host country currency",
                max_digits=14,
                null=True,
            ),
        ),
    ]
