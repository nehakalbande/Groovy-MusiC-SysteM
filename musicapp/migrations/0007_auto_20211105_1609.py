# Generated by Django 2.1.2 on 2021-11-05 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0006_artist_fan_group'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artist_fan_group',
            old_name='song',
            new_name='singer',
        ),
    ]
