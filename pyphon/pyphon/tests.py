from django.test import TestCase, Client, RequestFactory
from django.http import JsonResponse
from pyphon.views import HomeView
from django.urls import reverse_lazy
from django.conf import settings
from bs4 import BeautifulSoup as Soup
from django.contrib.auth.models import User


class HomeTestCase(TestCase):

    def setUp(self):
        """Setup for tests."""
        self.client = Client()
        self.request = RequestFactory()

    def test_home_status(self):
        """Test that the home view is status 200."""
        req = self.request.get("/blah")
        user1 = User()
        user1.save()
        req.user = user1
        view = HomeView.as_view()
        response = view(req)
        self.assertTrue(response.status_code == 200)

    def test_home_buttons_are_there(self):
        """There should be four buttons!"""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        response = self.client.get("/")
        soup = Soup(response.content, 'html.parser')
        self.assertEqual(len(soup.find_all('li')), 4)
