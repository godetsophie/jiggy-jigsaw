# Generated by Django 4.0.1 on 2022-01-23 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_delete_getimage_alter_image_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='play'),
        ),
    ]