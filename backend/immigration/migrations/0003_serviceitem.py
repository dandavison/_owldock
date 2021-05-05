# Generated by Django 3.2 on 2021-05-05 15:27

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('immigration', '0002_processstep_government_fee'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(help_text='Description of the service item')),
                ('process_step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='immigration.processstep')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]