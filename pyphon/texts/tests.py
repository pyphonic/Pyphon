from django.test import TestCase, Client, RequestFactory
from django.urls import reverse_lazy

from texts.models import Text
from texts.views import TextView

import datetime

class TextTestCase(TestCase):
    """The Text app test runner."""

    def setUp(self):
        """Text test setup."""
        self.client = Client()
        self.request = RequestFactory()

    def test_add_text_model(self):
        """Test that adding a text model works."""
        text1 = Text(body="Jabba no watta.", sender="them")
        text1.save()
        self.assertTrue(Text.objects.count() == 1)

    def test_add_two_text_models(self):
        """Test that adding two text models works."""
        text1 = Text(body="Jabba no watta.", sender="them")
        text1.save()
        text2 = Text(body="Too Nakma Noya Solo!", sender="you")
        text2.save()
        self.assertTrue(Text.objects.count() == 2)

    def test_image_body(self):
        """Test that text instance has correct body."""
        text1 = Text(body="Jabba no watta.", sender="them")
        text1.save()
        self.assertTrue(Text.objects.first().body == "Jabba no watta.")

    def test_image_time_format(self):
        """Test that text instance has correct time format."""
        text1 = Text(body="Jabba no watta.", sender="them")
        text1.save()
        # import pdb; pdb.set_trace()
        self.assertTrue(isinstance(Text.objects.first().time, datetime.datetime))

    def test_text_view_returns_text(self):
        """Test that text view returns a text."""
        text1 = Text(body="Jabba no watta.", sender="them")
        text1.save()
        text2 = Text(body="Too Nakma Noya Solo!", sender="you")
        text2.save()
        view = TextView.as_view()
        req = self.request.get(reverse_lazy('texts'))
        response = view(req)
        self.assertTrue(response.context_data['texts'].count() == 2)

    def test_text_view_returns_two_texts(self):
        """Test that text view returns two texts."""
        text1 = Text(body="Jabba no watta.", sender="them")
        text1.save()
        view = TextView.as_view()
        req = self.request.get(reverse_lazy('texts'))
        response = view(req)
        self.assertTrue(response.context_data['texts'].count() == 1)

    def test_text_view_status_200(self):
        """Test that text view returns ok status."""
        text1 = Text(body="Jabba no watta.", sender="them")
        text1.save()
        view = TextView.as_view()
        req = self.request.get(reverse_lazy('texts'))
        response = view(req)
        self.assertTrue(response.status_code == 200)
