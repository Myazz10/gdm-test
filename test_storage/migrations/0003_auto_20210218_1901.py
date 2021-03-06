# Generated by Django 3.1.6 on 2021-02-19 00:01

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_storage', '0002_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='mp4',
            field=models.FileField(blank=True, storage=cloudinary_storage.storage.VideoMediaCloudinaryStorage(), upload_to='videos/'),
        ),
    ]
