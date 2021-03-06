# Generated by Django 3.2 on 2021-05-07 22:57

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210507_1629'),
        ('immigration', '0006_auto_20210507_1309'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessRuleSetStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('sequence_number', models.PositiveIntegerField(help_text='Order of this step relative to other steps of this process.')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='processstep',
            name='host_country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.country'),
        ),
        migrations.AlterField(
            model_name='processstep',
            name='required_only_if_nationalities',
            field=models.ManyToManyField(blank=True, help_text='Applicant nationalities triggering requirement for this step. Blank means no nationality condition.', related_name='_immigration_processstep_required_only_if_nationalities_+', to='app.Country'),
        ),
        migrations.AlterField(
            model_name='route',
            name='host_country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routes_for_which_host_country', to='app.country'),
        ),
        migrations.AddConstraint(
            model_name='processstep',
            constraint=models.UniqueConstraint(fields=('host_country', 'name'), name='imm__process_step__host_country__name__uniq'),
        ),
        migrations.AddField(
            model_name='processrulesetstep',
            name='process_ruleset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='immigration.processruleset'),
        ),
        migrations.AddField(
            model_name='processrulesetstep',
            name='process_step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='immigration.processstep'),
        ),
        migrations.AddField(
            model_name='processruleset',
            name='process_steps',
            field=models.ManyToManyField(help_text='Available steps for this process.', through='immigration.ProcessRuleSetStep', to='immigration.ProcessStep'),
        ),
    ]
