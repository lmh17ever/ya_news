import pytest
from datetime import datetime, timedelta

from django.test.client import Client

from news.models import Comment, News
from news.constants import NEWS_COUNT_ON_HOME_PAGE


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(db):
    news = News.objects.create(
        title='Заголовок',
        text='Текст'
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        text='Текст',
        author=author
    )
    return comment


@pytest.fixture
def id_for_args(comment):
    return (comment.id,)


@pytest.fixture
def all_news(db):
    all_news = []
    for index in range(NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News(
            title=f'Новость {index}',
            text='Просто текст',
            date=datetime.today() - timedelta(days=index)
        )
        all_news.append(news)
    News.objects.bulk_create(all_news)
    return all_news


@pytest.fixture
def news_comments(news, author):
    news_comments = []
    for index in range(10):
        comments = Comment(
            news=news,
            text='Просто текст',
            author=author,
            created=datetime.today() - timedelta(days=index)
        )
        news_comments.append(comments)
    Comment.objects.bulk_create(news_comments)
    return news_comments


@pytest.fixture
def form_data(news, author):
    return {
        'news': news.id,
        'author': author.id,
        'text': 'Какой-то текст',
    }
