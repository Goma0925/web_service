# Generated by Django 2.0.1 on 2018-11-09 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_location_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='location_name',
            field=models.CharField(max_length=100),
        ),
    ]