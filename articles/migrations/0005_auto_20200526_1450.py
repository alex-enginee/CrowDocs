# Generated by Django 3.0.6 on 2020-05-26 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20200526_1436'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='article',
            name='one_title_many_versions',
        ),
    ]
