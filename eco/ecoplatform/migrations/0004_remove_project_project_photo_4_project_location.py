# Generated by Django 4.1.7 on 2023-03-22 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecoplatform', '0003_remove_problem_problem_photo_4_problem_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='project_photo_4',
        ),
        migrations.AddField(
            model_name='project',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
