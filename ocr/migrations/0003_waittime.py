# Generated by Django 3.1.5 on 2022-05-17 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0002_auto_20220509_0111'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaitTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.PositiveIntegerField()),
            ],
        ),
    ]
