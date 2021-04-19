# Generated by Django 3.2 on 2021-04-18 22:39

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=2)),
                ('unicode_flag', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProcessStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('sequence_number', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('logo_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='ProviderContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='StoredFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='uploads/%Y/%m/')),
                ('name', models.CharField(max_length=256)),
                ('media_type', models.CharField(max_length=128)),
                ('size', models.PositiveIntegerField()),
                ('charset', models.CharField(max_length=8, null=True)),
                ('application_file_type', models.CharField(choices=[('PROVIDER_CONTACT_UPLOAD', 'Provider Contact Upload')], max_length=64)),
                ('associated_object_uuid', models.UUIDField()),
                ('associated_object_content_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.contenttype')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='service',
            constraint=models.UniqueConstraint(fields=('name',), name='service__name__unique_constraint'),
        ),
        migrations.AddField(
            model_name='route',
            name='host_country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='routes_for_which_host_country', to='app.country'),
        ),
        migrations.AddField(
            model_name='providercontact',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.provider'),
        ),
        migrations.AddField(
            model_name='providercontact',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='provider',
            name='routes',
            field=models.ManyToManyField(related_name='providers', to='app.Route'),
        ),
        migrations.AddField(
            model_name='processstep',
            name='process',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='steps', to='app.process'),
        ),
        migrations.AddField(
            model_name='processstep',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.service'),
        ),
        migrations.AddField(
            model_name='process',
            name='home_country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='processes_for_which_home_country', to='app.country'),
        ),
        migrations.AddField(
            model_name='process',
            name='nationality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='processes_for_which_nationality', to='app.country'),
        ),
        migrations.AddField(
            model_name='process',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='processes', to='app.route'),
        ),
        migrations.AddConstraint(
            model_name='country',
            constraint=models.UniqueConstraint(fields=('name',), name='country__name__unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='country',
            constraint=models.UniqueConstraint(fields=('code',), name='country__code__unique_constraint'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddConstraint(
            model_name='storedfile',
            constraint=models.UniqueConstraint(fields=('name',), name='stored_file__name__unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='route',
            constraint=models.UniqueConstraint(fields=('name', 'host_country'), name='route__host_country__name__unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='providercontact',
            constraint=models.UniqueConstraint(fields=('user',), name='provider_contact__user__unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='provider',
            constraint=models.UniqueConstraint(fields=('name',), name='provider__name__unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='processstep',
            constraint=models.UniqueConstraint(fields=('process_id', 'sequence_number'), name='process_step__process__sequence_number__unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='processstep',
            constraint=models.UniqueConstraint(fields=('process_id', 'service'), name='process_step__process__service__unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='process',
            constraint=models.UniqueConstraint(fields=('home_country', 'nationality', 'route'), name='process__home_country__nationality__route__unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(fields=('email',), name='user__email__unique_constraint'),
        ),
    ]