# Generated by Django 4.0.1 on 2022-01-23 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_tile_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tile',
            name='is_blank',
        ),
        migrations.RemoveField(
            model_name='tile',
            name='test',
        ),
    ]
