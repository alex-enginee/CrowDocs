# Generated by Django 3.0.6 on 2020-05-21 08:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='avatar',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avatars', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
