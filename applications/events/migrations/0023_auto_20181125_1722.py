# Generated by Django 2.0.1 on 2018-11-25 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_event_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='picture',
            field=models.ImageField(default='place_holders/place_holder_700x400.png', upload_to='event_images/'),
        ),
    ]