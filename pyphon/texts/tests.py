from django.test import TestCase, Client, RequestFactory
from django.urls import reverse_lazy

from texts.models import Text
from texts.views import TextView, ProcessHookView

from contacts.models import Contact

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

    def test_text_repr_is_body(self):
        """Test that texts are properly represented."""
        text1 = Text(body="No bata tu tu, muni, muni.", sender="them")
        text1.save()
        self.assertTrue(text1.__str__() == text1.body[:20])

    # def test_text_view_returns_text(self):
    #     """Test that text view returns a text."""
    #     text1 = Text(body="Jabba no watta.", sender="them")
    #     text1.save()
    #     text2 = Text(body="Too Nakma Noya Solo!", sender="you")
    #     text2.save()
    #     view = TextView.as_view()
    #     req = self.request.get(reverse_lazy('texts', kwargs={"pk": "1"}))
    #     import pdb; pdb.set_trace()
    #     response = view(req)
    #     self.assertTrue(response.context_data['texts'].count() == 2)

    # def test_text_view_returns_two_texts(self):
    #     """Test that text view returns two texts."""
    #     text1 = Text(body="Jabba no watta.", sender="them")
    #     text1.save()
    #     view = TextView.as_view()
    #     req = self.request.get(reverse_lazy('texts'))
    #     response = view(req)
    #     self.assertTrue(response.context_data['texts'].count() == 1)

    # def test_text_view_status_200(self):
    #     """Test that text view returns ok status."""
    #     text1 = Text(body="Jabba no watta.", sender="them")
    #     text1.save()
    #     view = TextView.as_view()
    #     req = self.request.get(reverse_lazy('texts'))
    #     response = view(req)
    #     self.assertTrue(response.status_code == 200)

    # def test_text_view_template(self):
    #     """Test that text view uses texts template."""
    #     text1 = Text(body="Jabba no watta.", sender="them")
    #     text1.save()
    #     response = self.client.get(reverse_lazy('texts'))
    #     self.assertTemplateUsed(response, 'texts/texting.html')

# Needs tests that use self.client and bs4 to count texts on page

    def create_new_contact(self):
        """Create a contact for testing."""
        jabba = Contact(number='+15005550006')
        jabba.save()
        return jabba.id

    def submit_new_text_form(self):
        """Submit a new text form."""
        contact_id = self.create_new_contact()
        response = self.client.post(reverse_lazy('texts', kwargs={'pk': contact_id},), {'body': '6 Ploon, toh eenteen. Il yabba ma dookee Mahs tah, icht boong'})
        return response

    def test_add_a_text_count(self):
        """Test that adding a text increases the model count."""
        texts = Text.objects.count()
        self.submit_new_text_form()
        assert Text.objects.count() == texts + 1

    # receiving texts

    def test_get_request_on_hook_view_not_allowed(self):
        """Get request is not allowed on text_hook url."""
        request = self.client.get(reverse_lazy('text_hook'))
        self.assertEqual(request.status_code, 405)

    def test_post_request_to_text_hook_status_code(self):
        """A post request with correct kwargs returns a status code of 200."""
        req = self.client.post(reverse_lazy('text_hook'), {
            'Body': 'ToCountry=US&ToState=&FromCity=SEATTLE&Body=Test&FromCountry=US&To=%2B11111111111&From=%2B12064190136&ApiVersion=2010-04-01'})
        self.assertEqual(req.status_code, 200)

    def test_post_request_to_text_hook_create_new_contact(self):
        """Test a new contact is added when a text from unknown number is received."""
        old_contacts = Contact.objects.count()
        self.client.post(reverse_lazy('text_hook'), {
            'Body': 'ToCountry=US&ToState=&FromCity=SEATTLE&Body=Test&FromCountry=US&To=%2B1222222222&From=%2B12064190136&ApiVersion=2010-04-01'})
        contacts = Contact.objects.count()
        self.assertGreater(contacts, old_contacts)
