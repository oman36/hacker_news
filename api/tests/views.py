import json

from django.http import JsonResponse
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from api.forms import ORDER_CHOICES
from api.models import News

client = Client()


class PostsViewTests(TestCase):
    def setUp(self):
        now = timezone.make_aware(timezone.datetime(2019, 1, 1, 0, 0, 0), timezone.get_default_timezone())

        self._posts = []
        for i in range(10):
            now += timezone.timedelta(minutes=i)
            post = {
                'url': f'url{i}',
                'title': f'title{i}',
                'created': now.isoformat()
            }
            self._posts.append(post)
            n = News(**post)
            n.save()
            post['id'] = n.id
            n.created = now
            n.save()

    def test_no_params(self):
        response = self.client.get(reverse('api:posts'))
        self._test_json_response(response, 200)
        data = json.loads(response.content)
        self.assertEqual(data, self._posts[:5])

    def _test_json_response(self, response, status):
        self.assertEqual(response.status_code, status,
                         f'Request has status {response.status_code} instead of {status}')
        self.assertIsInstance(response, JsonResponse, f'Request return {type(response)} instead of JsonResponse')

    def test_order(self):
        response = self.client.get(reverse('api:posts') + '?order=unknown')
        self._test_400(response, 'order', 'Select a valid choice. unknown is not one of the available choices.')

        for choice, choice in ORDER_CHOICES:
            if choice.startswith('-'):
                continue
            response = self.client.get(reverse('api:posts') + f'?order={choice}')
            self._test_json_response(response, 200)
            data = json.loads(response.content)
            self.assertEqual(data, sorted(self._posts, key=lambda i: i[choice])[:5],
                f'Sorting by "{choice} ASC" does not work.')

            response = self.client.get(reverse('api:posts') + f'?order=-{choice}')
            self._test_json_response(response, 200)
            data = json.loads(response.content)
            self.assertEqual(data, sorted(self._posts, key=lambda i: i[choice], reverse=True)[:5],
                f'Sorting by "{choice} DESC" does not work.')

    def _test_400(self, response, field, message):
        self._test_json_response(response, 400)
        data = json.loads(response.content)
        self.assertIn('errors', data, 'Response with status 400 does not contain "errors"')
        self.assertIn(field, data['errors'], f'Response with status 400 does not contain info about {field}\'s errors')
        self.assertIn(message, data['errors'][field], 'Response with status 400 does not contain valid error message')

    def test_limit(self):
        response = self.client.get(reverse('api:posts') + '?limit=unknown')
        self._test_400(response, 'limit', 'Enter a whole number.')
        response = self.client.get(reverse('api:posts') + '?limit=-1')
        self._test_400(response, 'limit', 'Ensure this value is greater than or equal to 1.')

        response = self.client.get(reverse('api:posts') + f'?limit=2')
        self._test_json_response(response, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2, f'Limit does not work.')

    def test_offset(self):
        response = self.client.get(reverse('api:posts') + '?offset=unknown')
        self._test_400(response, 'offset', 'Enter a whole number.')
        response = self.client.get(reverse('api:posts') + '?offset=-1')
        self._test_400(response, 'offset', 'Ensure this value is greater than or equal to 0.')

        response = self.client.get(reverse('api:posts') + f'?offset=2')
        self._test_json_response(response, 200)
        data = json.loads(response.content)
        self.assertEqual(data[0], self._posts[2], f'Offset work incorrectly.')
