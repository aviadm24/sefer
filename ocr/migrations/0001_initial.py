# Generated by Django 3.1.5 on 2022-03-14 08:54

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='CameraConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='CameraDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Light',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='TaharaImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('release_date', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('logo', models.TextField(blank=True)),
                ('image', cloudinary.models.CloudinaryField(default=None, max_length=255, verbose_name='image')),
                ('image2', cloudinary.models.CloudinaryField(default=None, max_length=255, verbose_name='image2')),
                ('showed_to', models.CharField(blank=True, choices=[], max_length=250, null=True)),
                ('user_agent', models.CharField(blank=True, max_length=1000, null=True)),
                ('place_holder', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('color_percentage', models.JSONField(default={})),
                ('camera_config', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ocr.cameraconfig', verbose_name='פרטי הצילום')),
                ('camera_device', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ocr.cameradevice', verbose_name='ממה צולם')),
                ('comment', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ocr.comment', verbose_name='הערות')),
                ('first_pesak', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ocr_taharaimage_first_pesak', to='ocr.answers')),
                ('light', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ocr.light', verbose_name='תאורה')),
                ('rabbi_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('second_pesak', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ocr_taharaimage_second_pesak', to='ocr.answers', verbose_name='פסק')),
            ],
        ),
    ]
