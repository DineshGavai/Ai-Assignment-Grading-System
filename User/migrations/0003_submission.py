# Generated by Django 5.1.6 on 2025-02-27 09:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_assignment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='submissions/%Y/%m/%d/')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('status', models.CharField(choices=[('submitted', 'Submitted'), ('graded', 'Graded'), ('pending', 'Pending')], default='submitted', max_length=10)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.assignment')),
                ('student', models.ForeignKey(limit_choices_to={'role': 'student'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
