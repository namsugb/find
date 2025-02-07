# Generated by Django 5.1.4 on 2025-01-10 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='chaneel_id',
        ),
        migrations.AddField(
            model_name='channel',
            name='channel_id',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='channel',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
    ]
