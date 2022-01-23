"""
Definition of models.
"""

from django.db import models

class PlayImage(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='play')
    class Meta:
        db_table = "play_image"
