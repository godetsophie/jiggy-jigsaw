"""
Definition of models.
"""

import datetime
from distutils.command.upload import upload
from operator import mod
from django.conf import settings
from django.db import models

class PlayImage(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='play')
    level = models.IntegerField(default=3)
    class Meta:
        db_table = "play_image"

class Tile(models.Model):
    id = models.AutoField(primary_key=True)
    x = models.IntegerField()
    y = models.IntegerField()
    parent = models.ForeignKey(PlayImage, on_delete=models.CASCADE, related_name='tiles')
    image = models.ImageField(upload_to='tile')
    is_blank = models.BooleanField(default=False)
    class Meta:
        db_table = "tile"

class Game(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'user')
    play_image = models.ForeignKey(PlayImage, on_delete=models.CASCADE, related_name='play_image')
    success = models.BooleanField(default=False)
    class Meta:
        db_table = 'game'