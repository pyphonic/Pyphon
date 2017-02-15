from django.test import TestCase, Client, RequestFactory
from django.http import JsonResponse
from calls.views import call, callview, get_token
from django.urls import reverse_lazy
from django.conf import settings
from twilio.rest import TwilioRestClient
from bs4 import BeautifulSoup as Soup


class OutgoingCallTestCase(TestCase):

    def setUp(self):
        """Setup for tests."""
        self.client = Client()
        self.request = RequestFactory()

    def test_calls_route_status(self):
        """Test that routing to calls/ produces a 200 status."""
        req = self.request.get("/calls")
        view = callview
        response = view(req)
        self.assertTrue(response.status_code == 200)

    # def test_answered_route_status(self):
    #     """Test that routing to answered/ produces a 200 status."""
    #     req = self.request.get("/answered")
    #     view = answered
    #     response = view(req, "+15555555555")
    #     self.assertTrue(response.status_code == 200)

    # def test_answered_route_contains_hangup_button(self):
    #     """Test that routing to answered/ has a hangup button on the page."""
    #     req = self.request.get("/answered")
    #     view = answered
    #     response = view(req, "+15555555555")
    #     self.assertTrue(b'<div id="hangup">' in response.content)

    def test_calls_call_has_callerid_in_twiml(self):
        """Test that routing to calls/call returns TwiMl response object."""
        from django.conf import settings
        req = self.request.post("/calls/call", {
            'phoneNumber': '+15005550006'
        })
        view = call
        response = view(req)
        self.assertTrue('<Dial callerId="{}">'.format(
            settings.TWILIO_NUMBER) in response.content.decode('utf-8'))

    def test_get_token_returns_json_object_with_str_content(self):
        """Test that get_token returns a json object whose content is a str."""
        req = self.request.get("/token")
        view = get_token
        response = view(req)
        self.assertTrue(type(response.content.decode('utf-8')) is str)

    def test_get_token_returns_json_object(self):
        """Test that get_token returns a json object."""
        req = self.request.get("/token")
        view = get_token
        response = view(req)
        self.assertTrue(type(response) is JsonResponse)

    def test_get_token_contains_token(self):
        """Test that get_token actually returns a token key-value pair."""
        req = self.request.get("/token")
        view = get_token
        response = view(req)
        self.assertTrue(b'token' in response.content)


class IncomingCallTestCase(TestCase):

    def setUp(self):
        """Setup for tests."""
        self.client = Client()
        self.request = RequestFactory()
        self.twilio_client = TwilioRestClient(
            settings.TEST_ACCOUNT_SID,
            settings.TEST_AUTH_TOKEN)

    def test_incoming_call_doesnt_have_callerid_in_twiml(self):
        """Test that routing to calls/call returns TwiMl response object."""
        req = self.request.post("/calls/call")
        view = call
        response = view(req)
        self.assertTrue('<Dial>' in response.content.decode('utf-8'))
