# Generated by Django 4.0.4 on 2023-04-10 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecoplatform', '0009_remove_comment_dislikes_remove_comment_likes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='project_photo_1',
        ),
        migrations.RemoveField(
            model_name='project',
            name='project_photo_2',
        ),
        migrations.RemoveField(
            model_name='project',
            name='project_photo_3',
        ),
        migrations.RemoveField(
            model_name='project',
            name='project_photo_main',
        ),
        migrations.AddField(
            model_name='project',
            name='Gmail',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='instagram',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='linkedin',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='sponsor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='twitter',
            field=models.URLField(blank=True, null=True),
        ),
    ]