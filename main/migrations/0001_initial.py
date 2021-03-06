# Generated by Django 2.0.3 on 2018-03-26 02:12

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('landline1', models.CharField(max_length=30)),
                ('network_provider1', models.CharField(blank=True, default='', max_length=10)),
                ('landline2', models.CharField(blank=True, max_length=30)),
                ('network_provider2', models.CharField(blank=True, default='', max_length=10)),
                ('referred_by', models.EmailField(blank=True, max_length=30)),
                ('referral_count', models.IntegerField(default=0)),
                ('credit_count', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Ambime User',
                'verbose_name_plural': 'Ambime Users',
                'db_table': 'ambime_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Call_History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=30)),
                ('town', models.CharField(max_length=50)),
                ('county', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('cli', models.CharField(max_length=50)),
                ('call_result', models.CharField(max_length=50)),
                ('duration', models.CharField(max_length=50)),
                ('time_to_answer', models.CharField(max_length=50)),
                ('call_time', models.CharField(max_length=50)),
                ('date', models.DateField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Call History',
                'verbose_name_plural': 'Call History',
                'db_table': 'call_history',
            },
        ),
        migrations.CreateModel(
            name='RegistrationProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_key', models.CharField(max_length=40, verbose_name='activation key')),
                ('activated', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'registration profile',
                'verbose_name_plural': 'registration profiles',
                'db_table': 'registration_profile',
            },
        ),
        migrations.CreateModel(
            name='SupervisedRegistrationProfile',
            fields=[
                ('registrationprofile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.RegistrationProfile')),
            ],
            bases=('main.registrationprofile',),
        ),
        migrations.AddField(
            model_name='registrationprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
