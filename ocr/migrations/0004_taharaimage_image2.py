# Generated by Django 3.1.5 on 2022-03-02 09:36

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0003_auto_20220302_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='taharaimage',
            name='image2',
            field=cloudinary.models.CloudinaryField(default=None, max_length=255, verbose_name='image2'),
        ),
    ]