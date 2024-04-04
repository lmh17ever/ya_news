import pytest

from django.urls import reverse

from news.forms import CommentForm


@pytest.mark.django_db
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
):
    url = reverse('news:detail', args=(news.id,))
    response = parametrized_client.get(url)
    assert ('form' in response.context) == page_contains_comment_form
    if page_contains_comment_form:
        assert isinstance(response.context['form'], CommentForm)


@homepage_for_paginator_test
def test_paginator(homepage_for_paginator_test):
    homepage_for_paginator_test()
