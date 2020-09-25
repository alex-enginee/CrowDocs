# Generated by Django 3.0.6 on 2020-05-28 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0008_show_article'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.IntegerField(default=1, verbose_name='Article version')),
                ('pure_text', models.TextField(verbose_name='Article text')),
                ('date_updated', models.DateTimeField(default=None, verbose_name='Update date')),
            ],
        ),
        migrations.DeleteModel(
            name='Show_Article',
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['date_added', 'user_commentator'], 'verbose_name': 'Comment', 'verbose_name_plural': 'Comments'},
        ),
        migrations.RemoveConstraint(
            model_name='article',
            name='one_title_many_versions',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='author',
            new_name='user_author',
        ),
        migrations.RemoveField(
            model_name='article',
            name='article_version',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='author_name',
        ),
        migrations.AddField(
            model_name='comment',
            name='user_commentator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='description',
            field=models.CharField(default='', max_length=200, verbose_name='Topic description'),
        ),
        migrations.AlterField(
            model_name='article',
            name='article_title',
            field=models.CharField(max_length=100, unique=True, verbose_name='Article title'),
        ),
        migrations.AddField(
            model_name='articleversion',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.Article'),
        ),
        migrations.AddField(
            model_name='articleversion',
            name='user_updater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]