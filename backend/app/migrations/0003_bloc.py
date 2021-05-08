# Generated by Django 3.2 on 2021-05-08 20:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210507_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bloc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='The name of this bloc', max_length=128)),
                ('countries', models.ManyToManyField(to='app.Country')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
