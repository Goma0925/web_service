# Generated by Django 2.0.1 on 2018-11-09 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20181109_0234'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='slug',
            field=models.SlugField(max_length=255, null=True),
        ),
    ]