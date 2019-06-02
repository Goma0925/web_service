# Generated by Django 2.1.3 on 2019-05-30 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20190120_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='language',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='location',
            name='address',
            field=models.CharField(default='', max_length=120),
        ),
        migrations.AlterField(
            model_name='location',
            name='location_name',
            field=models.CharField(default='', max_length=30),
        ),
    ]