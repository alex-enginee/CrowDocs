from django.contrib import admin

# my apps with models
from users.models import User, Avatar
from articles.models import Topic, Tag, Article, ArticleVersion, Comment

admin.site.register(User)
admin.site.register(Avatar)

admin.site.register(Topic)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(ArticleVersion)
admin.site.register(Comment)
