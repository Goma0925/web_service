# Generated by Django 2.1.3 on 2019-06-02 01:10

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190602_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hangouts_to_host',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list),
        ),
    ]
