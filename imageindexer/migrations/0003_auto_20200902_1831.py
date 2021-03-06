# Generated by Django 3.1.1 on 2020-09-02 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageindexer', '0002_auto_20200902_1643'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classifiedimage',
            old_name='image_file',
            new_name='imagefile',
        ),
        migrations.RenameField(
            model_name='indexedvideo',
            old_name='video_file',
            new_name='videofile',
        ),
        migrations.AddField(
            model_name='classifiedimage',
            name='classification_label',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='classifiedimage',
            name='time',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
