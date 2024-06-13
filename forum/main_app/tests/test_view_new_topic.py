# dj
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase

# internal
from ..models import Board, Topic, Post
from ..forms import NewTopicForm
from ..views import new_topic


class NewTopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        User.objects.create_user(username='sajjad', email='sajjad@daneshmand.com', password='Abcd123')
        self.url = reverse('new_topic', kwargs={'pk': self.board.pk})
        login_url = reverse('login')
        data = {'username': 'sajjad', 'password': 'Abcd123'}
        self.client.post(login_url, data=data)
        self.response = self.client.get(self.url)

    def test_new_topic_view_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': self.board.pk + 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve(f'/boards/{self.board.pk}/new/')
        self.assertEqual(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        self.client.post(self.url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        """
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        """
        response = self.client.post(self.url, {})
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_invalid_post_data_empty_fields(self):
        """
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        """
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)


class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board description')
        self.url = reverse('new_topic', kwargs={'pk': self.board.pk})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
