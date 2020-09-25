"""articles app"""

from django import forms

from .models import Topic, Article, ArticleVersion


class TopicSuggestForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = [
            'topic_name',
            'description',
        ]
        # labels = {
        #     'topic_name': '',
        #     'description': '',
        # }


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'article_title',
            'article_text',
        ]
        # labels = {}
        # widgets = {}


# class ArticleVersionForm(forms.ModelForm):
#     class Meta:
#         model = ArticleVersion
