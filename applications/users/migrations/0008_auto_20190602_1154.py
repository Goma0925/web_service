# Generated by Django 2.1.3 on 2019-06-02 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20190602_0117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='introduction',
            field=models.CharField(default='', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='where_you_live',
            field=models.CharField(default='', max_length=160, null=True),
        ),
    ]
