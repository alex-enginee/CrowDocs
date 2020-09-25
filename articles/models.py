"""articles app"""

from django.contrib.auth import get_user_model
from django.db import models


SHORT_LEN = 80
MED_LEN = 200


class Topic(models.Model):
    """A topic of different articles"""
    topic_name = models.CharField(
        max_length=100,
        null=False,
        unique=True,
        verbose_name="Topic name",
    )
    description = models.CharField(
        max_length=200,
        verbose_name="Topic description",
        default="",
    )
    date_added = models.DateTimeField(auto_now_add=True,)

    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
        ordering = ['topic_name']

    def __str__(self):
        return self.topic_name


class Tag(models.Model):
    """Class for represent tags to search articles"""
    tag_string = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        verbose_name="Tag"
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['tag_string']

    def __str__(self):
        return self.tag_string


class Article(models.Model):
    """Class for represent articles itself"""
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(Tag)

    article_title = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        verbose_name="Article title"
    )

    article_text = models.TextField(
        verbose_name="Article text"
    )
    date_added = models.DateTimeField(auto_now_add=True,)
    user_author = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        get_latest_by = 'date_added'
        ordering = ['date_added', 'article_title']
        # constraints = [
        #     models.UniqueConstraint(fields=['article_title', 'article_version'],
        #                             name='one_title_many_versions')
        # ]

    def __str__(self):
        return self.article_title

    def short_text(self):
        if len(str(self.article_text)) > SHORT_LEN:
            return self.article_text[:SHORT_LEN] + r'...'
        else:
            return self.article_text

    def med_text(self):
        if len(str(self.article_text)) > MED_LEN:
            return self.article_text[:MED_LEN] + r'...</i></a></p>'
        else:
            return self.article_text


class ArticleVersion(models.Model):
    """Class for represent article versions"""
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE
    )
    version = models.IntegerField(
        null=False,
        default=1,
        verbose_name='Article version',
    )
    pure_text = models.TextField(
        verbose_name="Article text",
    )
    date_updated = models.DateTimeField(
        default=None,
        verbose_name='Update date',
    )
    user_updater = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Article version'
        verbose_name_plural = 'Article versions'
        get_latest_by = 'version'

    def __str__(self):
        return self.article.article_title + f" v.{self.version}"


class Comment(models.Model):
    """Class for represent comments for articles"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user_commentator = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    comment_text = models.CharField(
        max_length=500,
        null=False,
        verbose_name="Comment"
    )
    date_added = models.DateTimeField(auto_now_add=True, )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['date_added', 'user_commentator']

    def __str__(self):
        return self.comment_text
