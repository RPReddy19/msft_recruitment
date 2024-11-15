# Generated by Django 5.1.2 on 2024-11-02 19:04

import image_cropping.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_member_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='avatar',
            field=image_cropping.fields.ImageCropField(blank=True, default='static\\\\images\\userIcon.png', null=True, upload_to='avatars', verbose_name='Avatar'),
        ),
    ]
