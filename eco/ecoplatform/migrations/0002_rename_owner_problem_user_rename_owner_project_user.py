# Generated by Django 4.1.7 on 2023-03-14 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecoplatform', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problem',
            old_name='owner',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='owner',
            new_name='user',
        ),
    ]
