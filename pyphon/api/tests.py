from django.test import TestCase, Client, RequestFactory
from api.views import TextViewSet
from texts.models import Text

# Create your tests here.


class ApiTestCase(TestCase):

    def setUp(self):
        """Setup for tests."""
        self.client = Client()
        self.request = RequestFactory()

    def test_api_texts_view_status_ok(self):
        """Test api texts view is status ok."""
        request = self.request.get('/sf')
        view = TextViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_queryset_is_all_texts(self):
        """Text view should show all texts."""
        texts = self.client.get('/api/texts/')
        self.assertEqual(len(texts.json()), 0)
        text1 = Text(body="Jabba no watta.", sender="them")
        text1.save()
        texts = self.client.get('/api/texts/')
        self.assertEqual(len(texts.json()), 1)
