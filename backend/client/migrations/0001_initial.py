# Generated by Django 3.2 on 2021-05-03 13:29

import app.models
import app.models.process
import app.models.provider
from django.db import migrations, models
import django.db.models.deletion
import django_fsm
import owldock.models.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('user_uuid', owldock.models.fields.UUIDPseudoForeignKeyField(app.models.User, db_index=True, to_field='uuid')),
                ('home_country_uuid', owldock.models.fields.UUIDPseudoForeignKeyField(app.models.process.Country, db_index=True, to_field='uuid')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicantNationality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('country_uuid', owldock.models.fields.UUIDPseudoForeignKeyField(app.models.process.Country, db_index=True, to_field='uuid')),
            ],
            options={
                'verbose_name_plural': 'ApplicantNationalities',
            },
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('process_uuid', owldock.models.fields.UUIDPseudoForeignKeyField(app.models.process.Process, db_index=True, to_field='uuid')),
                ('target_entry_date', models.DateField()),
                ('target_exit_date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CaseStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('process_step_uuid', owldock.models.fields.UUIDPseudoForeignKeyField(app.models.process.ProcessStep, db_index=True, to_field='uuid')),
                ('sequence_number', models.PositiveIntegerField()),
                ('state_name', django_fsm.FSMField(default='FREE', max_length=50, protected=True)),
            ],
            options={
                'ordering': ['sequence_number'],
            },
        ),
        migrations.CreateModel(
            name='CaseStepContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('provider_contact_uuid', owldock.models.fields.UUIDPseudoForeignKeyField(app.models.provider.ProviderContact, db_index=True, to_field='uuid')),
                ('accepted_at', models.DateTimeField(null=True)),
                ('rejected_at', models.DateTimeField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('entity_domain_name', models.CharField(max_length=128)),
                ('logo_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='ClientProviderRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('provider_uuid', owldock.models.fields.UUIDPseudoForeignKeyField(app.models.provider.Provider, db_index=True, to_field='uuid')),
                ('preferred', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
            ],
            options={
                'ordering': ['-preferred'],
            },
        ),
        migrations.CreateModel(
            name='ClientContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('user_uuid', owldock.models.fields.UUIDPseudoForeignKeyField(app.models.User, db_index=True, to_field='uuid')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
            ],
        ),
        migrations.AddConstraint(
            model_name='client',
            constraint=models.UniqueConstraint(fields=('name',), name='client__name__unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='client',
            constraint=models.UniqueConstraint(fields=('entity_domain_name',), name='client__entity_domain_name__unique_constraint'),
        ),
        migrations.AddField(
            model_name='casestepcontract',
            name='case_step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.casestep'),
        ),
        migrations.AddField(
            model_name='casestep',
            name='active_contract',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.casestepcontract'),
        ),
        migrations.AddField(
            model_name='casestep',
            name='case',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='client.case'),
        ),
        migrations.AddField(
            model_name='case',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.applicant'),
        ),
        migrations.AddField(
            model_name='case',
            name='client_contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.clientcontact'),
        ),
        migrations.AddField(
            model_name='applicantnationality',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.applicant'),
        ),
        migrations.AddField(
            model_name='applicant',
            name='employer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client'),
        ),
        migrations.AlterUniqueTogether(
            name='clientproviderrelationship',
            unique_together={('client', 'provider_uuid')},
        ),
        migrations.AddConstraint(
            model_name='clientcontact',
            constraint=models.UniqueConstraint(fields=('user_uuid',), name='client_contact__user_uuid__unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='applicantnationality',
            constraint=models.UniqueConstraint(fields=('applicant', 'country_uuid'), name='applicant_nationality__applcant__country_uuid__unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='applicant',
            constraint=models.UniqueConstraint(fields=('user_uuid',), name='applicant__user_uuid__unique_constraint'),
        ),
    ]
