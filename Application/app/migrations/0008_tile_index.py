# Generated by Django 4.0.1 on 2022-01-25 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_game_remove_tile_name_remove_tile_new_x_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tile',
            name='index',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
