# Generated by Django 2.0.1 on 2018-11-24 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_remove_event_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.CharField(default='', max_length=50),
        ),
    ]