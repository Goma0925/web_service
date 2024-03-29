# Generated by Django 2.1.3 on 2019-01-20 16:45

import applications.users.models
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


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
                ('email', models.EmailField(max_length=254, unique=True)),
                ('watch_list', django.contrib.postgres.fields.jsonb.JSONField(default=list)),
                ('hangouts_to_join', django.contrib.postgres.fields.jsonb.JSONField(default=list)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user is a team staff.')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')),
                ('date_joined', models.DateTimeField(default=None, help_text='Time when the user account is created.')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', applications.users.models.UserAccountManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=30)),
                ('last_name', models.CharField(default='', max_length=30)),
                ('middle_name', models.CharField(blank=True, default='', max_length=30)),
                ('birthday', models.DateField(null=True)),
                ('where_you_live', models.CharField(default='', max_length=160)),
                ('introduction', models.CharField(default='', max_length=300)),
                ('profile_image_storage_url', models.CharField(default='', max_length=160)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
