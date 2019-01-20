# Generated by Django 2.1.3 on 2019-01-20 21:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 20, 22, 56, 29, 700622, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 20, 21, 56, 29, 700580, tzinfo=utc)),
        ),
    ]
