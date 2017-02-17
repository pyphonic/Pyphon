from django.test import TestCase, Client, RequestFactory
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.conf import settings
from twilio.rest import TwilioRestClient
from bs4 import BeautifulSoup as Soup
import factory
import random

from calls.views import call, callview, get_token, CallListView
from calls.models import Call
from contacts.models import Contact
from contacts.tests import ContactFactory
from django.contrib.auth.models import User


class CallFactory(factory.django.DjangoModelFactory):
    """User factory for testing."""

    class Meta:
        """Call."""
        model = Call

    direction = random.choice(['outgoing', 'incoming'])


class CallTestCase(TestCase):

    def setUp(self):
        """Setup for tests."""
        self.client = Client()
        self.request = RequestFactory()
        self.contact = ContactFactory.create()
        self.twilio_client = TwilioRestClient(
            settings.TEST_ACCOUNT_SID,
            settings.TEST_AUTH_TOKEN)

# ----------------------------- BASE PAGE --------------------------------
    def test_calls_route_status_base_page(self):
        """Test that routing to calls/ produces a 200 status."""
        req = self.request.get("/calls")
        view = callview
        response = view(req)
        self.assertTrue(response.status_code == 200)

# ----------------------------- TWIML PAGE --------------------------------

    def test_twiml_page_has_ok_status(self):
        """Test that routing to the TWIML page produces a 200 status."""
        req = self.request.get("/calls/call")
        view = callview
        response = view(req)
        self.assertTrue(response.status_code == 200)

    def test_twiml_page_loads_dial_template_if_no_outgoing_call(self):
        """Test that the dial template loads if no request to TWIML."""
        req = self.request.get("/calls/call")
        view = callview
        response = view(req)
        self.assertTrue(
            "<title>\nMake a Call\n</title>" in response.content.decode())

    def test_outgoing_call_has_callerid_in_twiml(self):
        """Test that routing to calls/call returns TwiMl response object."""
        req = self.request.post("/calls/call", {
            'phoneNumber': '+15005550006'
        })
        view = call
        response = view(req)
        self.assertTrue('<Dial callerId="{}">'.format(
            settings.TWILIO_NUMBER) in response.content.decode('utf-8'))

    def test_incoming_call_doesnt_have_callerid_in_twiml(self):
        """Test that routing to calls/call returns TwiMl response object."""
        req = self.request.get("/calls/call", {'From': '12345678910'})
        view = call
        response = view(req)
        self.assertTrue('<Dial>' in response.content.decode('utf-8'))

    def test_new_call_instance_created_on_outgoing_call(self):
        """When outgoing call initiated, new call instance is created."""
        self.assertEqual(Call.objects.count(), 0)
        self.client.post(reverse_lazy('call'), {'phoneNumber': '+12345678910'})
        self.assertEqual(Call.objects.count(), 1)

    def test_new_call_instance_created_on_incoming_call(self):
        """When incoming call initiated, new call instance is created."""
        self.assertEqual(Call.objects.count(), 0)
        self.client.get(reverse_lazy('call'), {'From': '+12345678910'})
        self.assertEqual(Call.objects.count(), 1)

    def test_new_contact_created_on_call_if_new_number(self):
        """When call made or received, new contact is made if new number."""
        self.assertEqual(Contact.objects.count(), 1)
        self.client.post(reverse_lazy('call'), {'phoneNumber': '+12345678910'})
        self.assertEqual(Contact.objects.count(), 2)

    def test_new_contact_not_created_on_call_if_already_contact(self):
        """When call made, received to old number, new contact is not made."""
        self.assertEqual(Contact.objects.count(), 1)
        existing_number = str(self.contact.number).strip('+')
        self.client.post(
            reverse_lazy('call'), {'phoneNumber': existing_number})
        self.assertEqual(Contact.objects.count(), 1)

    def test_call_has_contact_outgoing_call(self):
        """When outgoing call initiated, new contact should have number."""
        self.client.post(reverse_lazy('call'), {'phoneNumber': '2345678910'})
        contact = Call.objects.first().contact
        self.assertEqual(contact.number, '+12345678910')

    def test_call_has_contact_incoming_call(self):
        """When incoming call initiated, new contact should have number."""
        self.client.get(reverse_lazy('call'), {'From': '+12345678910'})
        contact = Call.objects.first().contact
        self.assertEqual(contact.number, '+12345678910')

# ----------------------------- TOKEN PAGE --------------------------------

    def test_calls_route_status_token_page(self):
        """Test that routing to calls/dial produces a 200 status."""
        req = self.request.get("/calls/token")
        view = callview
        response = view(req)
        self.assertTrue(response.status_code == 200)

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

# ----------------------------- DIAL PAGE --------------------------------        

    def test_calls_route_status_dial_page(self):
        """Test that routing to calls/dial produces a 200 status."""
        req = self.request.get("/calls/dial")
        view = callview
        response = view(req)
        self.assertTrue(response.status_code == 200)

    def test_dial_route_loads_correct_template(self):
        """Test that the correct template gets loaded for the dial page."""
        req = self.request.get("/calls/dial")
        view = callview
        response = view(req)
        self.assertTrue(
            "<title>\nMake a Call\n</title>" in response.content.decode())

    def test_dial_page_loads_TWIML_on_form_submission(self):
        """Test that dial page loads TWIML when you call a phone number."""
        req = self.request.post("/calls/dial", {
            'phoneNumber': '+15005550006'
        })
        view = call
        response = view(req)
        self.assertTrue('<Dial callerId="{}">'.format(
            settings.TWILIO_NUMBER) in response.content.decode('utf-8'))

# ----------------------------- RECENT PAGE --------------------------------

    def test_recent_route_redirects_if_unauthorized(self):
        """Test that the recent calls list reroutes to login if unauth."""
        response = self.client.get('/calls/recent')
        self.assertEqual(response.status_code, 302)

    def test_call_list_status_ok(self):
        """Recent calls list should be status 200."""
        req = self.request.get("/calls/recent")
        req.user = ContactFactory.create()
        req.user.is_authenticated = True
        view = CallListView.as_view()
        response = view(req)
        self.assertEqual(response.status_code, 200)

    def test_call_list_shows_all_previous_calls(self):
        """Call history should show up in order on the call list view."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        response = self.client.get(reverse_lazy('call_list'))
        soup = Soup(response.content, 'html.parser')
        trs = soup.find_all('tr')
        call_length = len(trs)
        [CallFactory.create(contact=self.contact) for i in range(20)]
        response = self.client.get(reverse_lazy('call_list'))
        soup = Soup(response.content, 'html.parser')
        trs = soup.find_all('tr')
        self.assertEqual(len(trs), call_length + 20)

    def test_call_list_shows_correct_glyphicon_per_call_direction(self):
        """Test that calls list shows correct icon based on call direction."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        new_call = CallFactory.create(contact=self.contact)
        response = self.client.get(reverse_lazy('call_list'))
        soup = Soup(response.content, 'html.parser')
        # import pdb;pdb.set_trace()
        if new_call.direction == "incoming":
            span = soup.find_all(
                "span", {"class": "glyphicon glyphicon-log-in"})
            self.assertEqual(
                '<span aria-hidden="true" class="glyphicon glyphicon-log-in"></span>', str(span[0]))
        else:
            span = soup.find_all(
                "span", {"class": "glyphicon glyphicon-log-out"})
            self.assertEqual(
                '<span aria-hidden="true" class="glyphicon glyphicon-log-out"></span>', str(span[0]))