# Generated by Django 4.1.4 on 2023-02-18 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ocr', '0005_auto_20221225_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taharaimage',
            name='first_pesak',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_first_pesak', to='ocr.answers'),
        ),
        migrations.AlterField(
            model_name='taharaimage',
            name='second_pesak',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_second_pesak', to='ocr.answers', verbose_name='פסק'),
        ),
        migrations.CreateModel(
            name='LastSentImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('project_type', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('image_id', models.BigIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
