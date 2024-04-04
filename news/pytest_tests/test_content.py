import pytest
from http import HTTPStatus

from django.urls import reverse

from news.forms import CommentForm
from news.constants import NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.parametrize(
    'name',
    ('news:detail', 'news:edit')
)
@pytest.mark.parametrize(
    'parametrized_client, page_contains_comment_form',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('client'), False),
    )
)
def test_comment_form_on_page(
    parametrized_client,
    page_contains_comment_form,
    news,
    name,
    comment
):
    url = reverse(name, args=(news.id,))
    response = parametrized_client.get(url)
    if response.status_code == HTTPStatus.OK:
        assert ('form' in response.context) == page_contains_comment_form
        if page_contains_comment_form:
            assert isinstance(response.context['form'], CommentForm)


def test_paginator(all_news, client):
    url = reverse('news:home')
    responce = client.get(url)
    object_list = responce.context['object_list']
    news_count = object_list.count()
    assert news_count == NEWS_COUNT_ON_HOME_PAGE


def test_news_order(all_news, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comment_order(news_comments, client, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps
