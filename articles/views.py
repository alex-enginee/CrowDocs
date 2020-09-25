"""articles app"""

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import TopicSuggestForm, ArticleCreateForm
from .models import Topic, Article, ArticleVersion, Comment, Tag

from .custom_functions.script_obliterator import obliterate_scripts
from .custom_functions.ins_del_obliterator import obliterate_ins_dels
from .custom_functions.diff_highlighter import highlight_diff

TOPICS_PAGE = 'articles/topics.html'
TOPIC_ARTICLES_PAGE = 'articles/topic_articles.html'
ARTICLE_PAGE = 'articles/article.html'

NEW_TOPIC_PAGE = 'articles/new_topic.html'
NEW_ARTICLE_PAGE = 'articles/new_article.html'
EDIT_ARTICLE_PAGE = 'articles/edit_article.html'


# OUTPUT EXISTED

def topics(request):
    topics = Topic.objects.order_by('topic_name')

    return render(request, TOPICS_PAGE, context={
        'topics': topics
    })


def topic_articles(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    articles = topic.article_set.order_by('-date_added')

    return render(request, TOPIC_ARTICLES_PAGE, context={
        'topic': topic,
        'articles': articles,
    })


def article(request, article_id):
    article = Article.objects.get(id=article_id)

    try:
        article_version = article.articleversion_set.latest()
        if article_version.version == 1:
            article_version = None
    except:
        article_version = None

    return render(request, ARTICLE_PAGE, context={
        'article': article,
        'article_version': article_version,
    })


# CREATING NEW

@login_required
def new_topic(request):
    if request.method == 'GET':
        form = TopicSuggestForm()
        return render(request, NEW_TOPIC_PAGE, context={
            'form': form,
        })
    elif request.method == 'POST':
        form = TopicSuggestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("articles:topics")


@login_required
def new_article(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    if request.method == 'GET':
        form = ArticleCreateForm(initial={'topic': topic})
        return render(request, NEW_ARTICLE_PAGE, context={
            'topic': topic,
            'form': form,
        })
    elif request.method == 'POST':

        form = ArticleCreateForm(request.POST)
        raw_text = request.POST['article_text']
        purified_text = obliterate_scripts(raw_text)

        if form.is_valid():
            # Article logic
            added_article = form.save(commit=False)
            added_article.topic = topic
            added_article.user_author = request.user
            added_article.article_text = purified_text
            added_article.save()

            # Version of article logic
            current_version = ArticleVersion(
                article=added_article,
                pure_text=purified_text,
                date_updated=added_article.date_added,
                user_updater=added_article.user_author,
            )
            current_version.save()

            # return redirect('articles:topic_articles', topic_id)
            return redirect('articles:article', added_article.id)


@login_required
def edit_article(request, article_id):
    article = Article.objects.get(id=article_id)
    topic = article.topic

    if request.method == 'GET':
        form = ArticleCreateForm(instance=article)
        return render(request, EDIT_ARTICLE_PAGE, context={
            'topic': topic,
            'article': article,
            'form': form,
        })
    elif request.method == 'POST':
        form = ArticleCreateForm(instance=article, data=request.POST)

        raw_text = request.POST['article_text']
        scriptless_text = obliterate_scripts(raw_text)
        purified_text = obliterate_ins_dels(scriptless_text)

        if form.is_valid():
            # Article logic
            old_text = article.article_text
            edited_article = form.save(commit=False)

            # Version of article logic
            try:
                old_version = edited_article.articleversion_set.latest()
                new_version = ArticleVersion(
                    article=edited_article,
                    version=old_version.id + 1,
                    pure_text=purified_text,
                    date_updated=timezone.now(),
                    user_updater=request.user,
                )
                old_text = old_version.pure_text
            except:
                new_version = ArticleVersion(
                    article=edited_article,
                    version=2,
                    pure_text=purified_text,
                    date_updated=timezone.now(),
                    user_updater=request.user,
                )

            new_version.save()

            output_text = highlight_diff(old_text,
                                         purified_text,
                                         request.user,
                                         timezone.now())

            # Logic for output article
            edited_article.article_text = output_text
            edited_article.save()
            return redirect('articles:article', article.id)
