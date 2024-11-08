# Generated by Django 5.1.3 on 2024-11-07 04:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_user_avatar_user_bio_user_name_alter_user_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='topic',
        ),
        migrations.AddField(
            model_name='messages',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]