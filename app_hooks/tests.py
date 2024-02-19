from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Filter


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)

    def test_login(self):
        login_url = reverse('users:login')
        response = self.client.post(
            login_url, {'username': self.username, 'password': self.password})

        self.assertEqual(response.status_code, 302)

        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        logout_url = reverse('users:logout')
        response = self.client.post(logout_url)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(response.wsgi_request.user.is_authenticated)


class ModelTestCase(TestCase):
    def test_filter(self):
        filter = Filter(name='name', data='data')
        filter.save()

        filter_inst = Filter.objects.get(id=filter.id)

        self.assertEqual(filter_inst.name, 'name')
        self.assertEqual(filter_inst.data, 'data')
