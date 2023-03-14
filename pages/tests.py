from django.test import SimpleTestCase
from django.urls import reverse


class HomepageTests(SimpleTestCase):

    def test_homepage_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_url_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_template_is_used(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')
