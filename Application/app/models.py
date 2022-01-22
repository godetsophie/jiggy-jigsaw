"""
Definition of models.
"""

from django.db import models

class GetImage(models.Model):   
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to="media")
    class Meta:
        db_table = "pictures"


class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    def __str__(self):
        return self.title
    class Meta:
        db_table = "myapp_image"
