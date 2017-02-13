from django.test import TestCase, Client, RequestFactory
from django.urls import reverse_lazy

from texts.models import Text
from texts.views import TextView, decode_request_body, ProcessHookView

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
        self.assertTrue(text1.__repr__() == text1.body[:20])
    
    # def test_text_view_returns_text(self):
    #     """Test that text view returns a text."""
    #     text1 = Text(body="Jabba no watta.", sender="them")
    #     text1.save()
    #     text2 = Text(body="Too Nakma Noya Solo!", sender="you")
    #     text2.save()
    #     view = TextView.as_view()
    #     req = self.request.get(reverse_lazy('texts'))
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
        jabba = Contact(number='+15555555555')
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
    def test_decode_request_body_return_dict(self):
        """Test decode_request_body() returns a dictionary."""
        request_string = b'Body=Test&From=%2B15555555111'
        self.assertIsInstance(decode_request_body(request_string), dict)

    def test_decode_request_body_has_correct_keys(self):
        """Test decode_request_body() returns dict with correct keys."""
        request_string = b'Body=Test&From=%2B15555555111'
        request_dict = decode_request_body(request_string)
        self.assertTrue("From" in request_dict.keys())

    def test_From_key_has_valid_phone_number(self):
        """Test ["From"] has a valid phone number."""
        request_string = b'Body=Test&From=%2B15555555111'
        request_dict = decode_request_body(request_string)
        self.assertTrue(request_dict["From"][0] == '+15555555111')

    def test_Body_key_has_no_extra_char(self):
        """Test body value has no extra character."""
        request_string = b'Body=Test+test+test+test&From=%2B15555555111'
        request_dict = decode_request_body(request_string)
        self.assertEqual(request_dict["Body"][0], "Test test test test")

    def test_no_and_in_dict(self):
        """Test there is no "&" in the returned dictionary."""
        request_string = b'Body=Test+test+test+test&From=%2B15555555111'
        request_dict = decode_request_body(request_string)
        self.assertFalse("&" in request_dict)
