# Generated by Django 2.1.3 on 2019-06-02 01:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190530_0744'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='hangouts_to_join',
            new_name='join_list',
        ),
    ]
