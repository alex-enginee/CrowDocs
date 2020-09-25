"""articles app"""

from django.urls import path

from . import views

app_name = 'articles'


urlpatterns = [
    # here we go to see all topics on web site
    path('topics', views.topics, name='topics'),

    # and here to see articles in topic
    path('topic/<topic_id>', views.topic_articles, name='topic_articles'),

    # go there to see particular article
    path('article/<article_id>', views.article, name='article'),

    # section for creating new topic
    path('new_topic', views.new_topic, name='new_topic'),

    # section for creating new article with topic bound
    path('new_article/<topic_id>', views.new_article, name='new_article'),

    # section for editing article
    path('edit_article/<article_id>', views.edit_article, name='edit_article'),
]
