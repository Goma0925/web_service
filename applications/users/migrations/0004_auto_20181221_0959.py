# Generated by Django 2.1.3 on 2018-12-21 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_join_list'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='join_list',
            new_name='joined_hangouts',
        ),
    ]