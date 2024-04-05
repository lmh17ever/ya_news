from http import HTTPStatus

from pytest_django.asserts import assertRedirects, assertFormError
from django.urls import reverse
from django.forms.models import model_to_dict

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


def test_user_can_create_comment(author_client, author, form_data, news):
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, form_data)
    expected_url = reverse('news:detail', args=(news.id,)) + '#comments'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 1
    comment_to_dict = model_to_dict(Comment.objects.get())
    comment_dict_for_assert = {
        key: comment_to_dict[key] for key in form_data.keys()
    }
    assert comment_dict_for_assert == form_data


def test_anonymous_user_cant_create_comment(client, form_data, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.post(url, form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_user_cant_use_bad_words(author_client, news):
    bad_words_data = {
        'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'
    }
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_edit_comment(author_client, form_data, comment):
    url = reverse('news:edit', args=(comment.id,))
    response = author_client.post(url, form_data)
    expected_url = reverse(
        'news:detail', args=(comment.news.id,)
    ) + '#comments'
    assertRedirects(response, expected_url)
    comment.refresh_from_db()
    comment_to_dict = model_to_dict(comment)
    comment_dict_for_assert = {
        key: comment_to_dict[key] for key in form_data.keys()
    }
    assert comment_dict_for_assert == form_data


def test_other_user_cant_edit_comment(not_author_client, form_data, comment):
    url = reverse('news:edit', args=(comment.id,))
    response = not_author_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert model_to_dict(comment) == model_to_dict(comment_from_db)


def test_author_can_delete_comment(author_client, id_for_args):
    comment = Comment.objects.get(id=id_for_args[0])
    url = reverse('news:delete', args=id_for_args)
    response = author_client.post(url)
    expected_url = reverse(
        'news:detail', args=(comment.news.id,)
    ) + '#comments'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_other_user_cant_delete_comment(not_author_client, id_for_args):
    url = reverse('news:delete', args=id_for_args)
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
