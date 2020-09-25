# Generated by Django 3.0.6 on 2020-05-26 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_avatar_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='avatar',
            options={'get_latest_by': 'creation_date', 'ordering': ['creation_date']},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username', 'email']},
        ),
    ]
