# Generated by Django 3.2 on 2021-04-30 19:50

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssuedDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('proves_right_to_enter', models.BooleanField(default=False)),
                ('proves_right_to_reside', models.BooleanField(default=False)),
                ('proves_right_to_work', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IssuedDocumentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Name of this issued document type.', max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Name of this immigration process', max_length=128)),
                ('contract_location', models.CharField(blank=True, choices=[('HOME_COUNTRY', 'Home Country'), ('HOST_COUNTRY', 'Host Country')], help_text='Contract location for this process. Blank means no contract location condition.', max_length=16, null=True)),
                ('payroll_location', models.CharField(blank=True, choices=[('HOME_COUNTRY', 'Home Country'), ('HOST_COUNTRY', 'Host Country')], help_text='Payroll location for this process. Blank means no payroll location condition.', max_length=16, null=True)),
                ('minimum_salary', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='Minimum salary in host country currency')),
                ('duration_min_days', models.PositiveIntegerField(blank=True, help_text='Minimum visit duration (days) required for this process to be available. Blank means no minimum duration requirement.', null=True)),
                ('duration_max_days', models.PositiveIntegerField(blank=True, help_text='Maximum visit duration (days) allowed for this process to be available. Blank means no maximum duration limit.', null=True)),
                ('intra_company_relationship_required', models.BooleanField(default=False, help_text='Does this process apply only if the applicant will work in the host country for the same company as that for which they work in the    home country?')),
                ('home_countries', models.ManyToManyField(blank=True, help_text='Home countries for which this immigration process is available. Blank means this process is available for any home country.', related_name='processes_for_which_home_country', to='app.Country')),
                ('host_country', models.ForeignKey(help_text='Host country for this immigration process', on_delete=django.db.models.deletion.CASCADE, related_name='processes_for_which_host_country', to='app.country')),
                ('nationalities', models.ManyToManyField(blank=True, help_text='Applicant nationalities for which this immigration process is available. Blank means this process is available for any applicant nationality.', related_name='processes_for_which_nationality', to='app.Country')),
            ],
            options={
                'verbose_name_plural': 'Processes',
            },
        ),
        migrations.CreateModel(
            name='ProcessStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Name of this step', max_length=128)),
                ('sequence_number', models.PositiveIntegerField(help_text='Order of this step relative to other steps of this process.')),
                ('estimated_min_duration_days', models.PositiveIntegerField(help_text='Minimum number of days this step is expected to take')),
                ('estimated_max_duration_days', models.PositiveIntegerField(help_text='Maximum number of days this step is expected to take')),
                ('applicant_can_enter_host_country_after', models.BooleanField(default=False, help_text='Can the applicant enter the host country on completion of this step?')),
                ('applicant_can_work_after', models.BooleanField(default=False, help_text='Can the applicant work in the host country on completion of this step?')),
                ('required_only_if_payroll_location', models.CharField(blank=True, choices=[('HOME_COUNTRY', 'Home Country'), ('HOST_COUNTRY', 'Host Country')], help_text='Payroll location triggering requirement for this step. Blank means no payroll location condition.', max_length=16, null=True)),
                ('required_only_if_duration_exceeds', models.PositiveIntegerField(blank=True, help_text='Visit duration (days) triggering requirement for this step. Blank means no duration condition.', null=True)),
                ('issued_documents', models.ManyToManyField(blank=True, help_text='Issued documents associated with this process step.', through='immigration.IssuedDocument', to='immigration.IssuedDocumentType')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='immigration.process')),
                ('required_only_if_nationalities', models.ManyToManyField(blank=True, help_text='Applicant nationalities triggering requirement for this step. Blank means no nationality condition.', to='app.Country')),
            ],
        ),
        migrations.AddField(
            model_name='issueddocument',
            name='issued_document_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='immigration.issueddocumenttype'),
        ),
        migrations.AddField(
            model_name='issueddocument',
            name='process_step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='immigration.processstep'),
        ),
        migrations.AddConstraint(
            model_name='processstep',
            constraint=models.UniqueConstraint(fields=('process', 'name'), name='imm__process_step__name__uniq'),
        ),
        migrations.AddConstraint(
            model_name='process',
            constraint=models.UniqueConstraint(fields=('name', 'host_country'), name='imm__process__host_country_name__uniq'),
        ),
    ]
