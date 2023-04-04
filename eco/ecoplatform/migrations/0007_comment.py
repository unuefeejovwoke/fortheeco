# Generated by Django 4.1.7 on 2023-04-04 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecoplatform', '0006_problem_downvotes_problem_upvotes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ecoplatform.problem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['-created'],
            },
        ),
    ]
