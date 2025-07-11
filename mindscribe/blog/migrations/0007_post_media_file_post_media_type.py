# Generated by Django 5.2.4 on 2025-07-04 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_post_options_post_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='media_file',
            field=models.FileField(blank=True, null=True, upload_to='post_media/', verbose_name='Медиа-контент (фото, видео или GIF)'),
        ),
        migrations.AddField(
            model_name='post',
            name='media_type',
            field=models.CharField(blank=True, choices=[('image', 'Фото'), ('video', 'Видео'), ('gif', 'GIF')], max_length=5, null=True),
        ),
    ]
