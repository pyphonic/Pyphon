from django.test import TestCase, Client, RequestFactory
from django.http import JsonResponse
from calls.views import call, callview, get_token, answered
from django.urls import reverse_lazy


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

    def test_answered_route_status(self):
        """Test that routing to answered/ produces a 200 status."""
        req = self.request.get("/answered")
        view = answered
        response = view(req)
        self.assertTrue(response.status_code == 200)

    def test_answered_route_contains_hangup_button(self):
        """Test that routing to answered/ has a hangup button on the page."""
        req = self.request.get("/answered")
        view = answered
        response = view(req)
        self.assertTrue('<div id="hangup">' in response.content)

    def test_calls_call_has_callerid_in_twiml(self):
        """Test that routing to calls/call returns TwiMl response object."""
        from django.conf import settings
        req = self.request.get("/calls/call")
        view = call
        response = view(req)
        self.assertTrue('<Dial callerId="{}">'.format(
            settings.TWILIO_NUMBER) in response.content)

    def test_get_token_returns_json_object_with_str_content(self):
        """Test that get_token returns a json object whose content is a str."""
        req = self.request.get("/token")
        view = get_token
        response = view(req)
        self.assertTrue(type(response.content) is str)

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
        self.assertTrue('token' in response.content)

    # def test_call_function_returns_200_status(self):
    #     """Test that actually making a dummy call returns a status 200."""
    #     # req = self.request.get("/calls")
    #     # view = call
    #     params = {"phoneNumber": '+15556667777'}
    #     response = self.client.post('/call', data=params)
    #     self.assertTrue(response.status == "200")
