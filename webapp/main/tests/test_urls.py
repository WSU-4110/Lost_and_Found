from django.urls import reverse, resolve
from django.test import SimpleTestCase
from main.views import home

class UrlsTest(SimpleTestCase):
    def test_create_post(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)