# Generated by Django 3.1.5 on 2022-03-02 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0004_taharaimage_image2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taharaimage',
            name='second_pesak',
            field=models.CharField(blank=True, choices=[('good', 'טהור'), ('bad', 'טמא'), ('rabbi_q', 'שאלת רב'), ('cant_see', 'לא רואים ברור')], default='', max_length=250, null=True, verbose_name='פסק'),
        ),
        migrations.AlterField(
            model_name='taharaimage',
            name='showed_to',
            field=models.CharField(blank=True, choices=[('', ''), ('', ''), ('', '')], max_length=250, null=True),
        ),
    ]