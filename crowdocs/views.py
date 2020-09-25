"""crowdocs project"""

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator

from articles.models import Article

INDEX_PAGE = 'crowdocs/index.html'
ARTICLES_PER_PAGE = 10
LATEST_ARTICLES = 5


@require_GET
def index(request):
    user = request.user
    query = request.GET.get("q")
    page = request.GET.get("page", 1)
    if query:
        que_articles = Article.objects.filter(
            Q(article_title__icontains=query) | Q(article_text__icontains=query)
        ).order_by("-date_added")
        latest_articles = None
        # pagin_que = Paginator(que_articles, ARTICLES_PER_PAGE)
    else:
        que_articles = None
        latest_articles = Article.objects.order_by("-date_added")[:LATEST_ARTICLES]

    return render(request, INDEX_PAGE, context={
        'que_articles': que_articles,
        'latest_articles': latest_articles,
        'user': user
    })
