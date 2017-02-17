from django.test import TestCase, Client, RequestFactory
from django.urls import reverse_lazy
from api.views import (
    TextViewSet,
    CallViewSet,
    ContactViewSet,
    LastText,
    GetContactByNumber
)

from texts.models import Text
from calls.models import Call
from contacts.models import Contact
from contacts.tests import ContactFactory
from django.contrib.auth.models import User

# Create your tests here.


class ApiTestCase(TestCase):

    def setUp(self):
        """Setup for tests."""
        self.client = Client()
        self.request = RequestFactory()
        self.contacts = [ContactFactory.create() for i in range(10)]

    def test_api_texts_view_status_ok(self):
        """Test api texts view is status ok."""
        user1 = User()
        user1.save()
        request = self.request.get('/sf')
        request.user = user1
        view = TextViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_api_calls_view_status_ok(self):
        """Test api calls view is status ok."""
        user1 = User()
        user1.save()
        request = self.request.get('/sf')
        request.user = user1
        view = CallViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_api_contacts_list_view_status_ok(self):
        """Test api contacts list view is status ok."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        request = self.request.get('/sf')
        request.user = user1
        view = ContactViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_api_contacts_detail_view_status_ok(self):
        """Test api contacts detail view is status ok."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        jabba = Contact(name="Jabba", number="+12068675309")
        jabba.save()
        request = self.request.get(reverse_lazy('api_contacts_retrieve',
                                   kwargs={"pk": jabba.pk}))
        request.user = user1
        view = ContactViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=jabba.id)
        self.assertEqual(response.status_code, 200)

    def test_api_last_text_view_status_ok(self):
        """Test api contacts view is status ok."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        request = self.request.get('/sf')
        request.user = user1
        text1 = Text(body="Jabba no watta.", sender="them")
        text1.save()
        view = LastText.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_api_get_contact_by_number_view_status_ok(self):
        """Test api contacts view is status ok."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        number = str(self.contacts[0].number)[1:]
        request = self.request.get('/sf', number=number)
        request.user = user1
        view = GetContactByNumber.as_view()
        response = view(request, number=number)
        self.assertEqual(response.status_code, 200)

    def test_text_queryset_is_all_texts(self):
        """Text view should show all texts."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        texts = self.client.get('/api/texts/')
        self.assertEqual(len(texts.json()), 0)
        text1 = Text(body="Jabba no watta.", sender="them")
        text1.save()
        texts = self.client.get('/api/texts/')
        self.assertEqual(len(texts.json()), 1)

    def test_contact_queryset_is_all_contacts(self):
        """Contact view should show all contacts."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        contacts = self.client.get('/api/texts/')
        self.assertEqual(len(contacts.json()), 0)
        jabba = Contact(name="Jabba", number="+2068675309")
        jabba.save()
        contacts = self.client.get('/api/contacts/list/')
        self.assertEqual(len(contacts.json()), 11)

    def test_call_queryset_is_all_calls(self):
        """Call view should show all texts."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        calls = self.client.get('/api/calls/')
        self.assertEqual(len(calls.json()), 0)
        jabba = Contact(name="Jabba", number="+12068675309")
        jabba.save()
        call1 = Call(contact=jabba, direction="outgoing", status="completed")
        call1.save()
        calls = self.client.get('/api/calls/')
        self.assertEqual(len(calls.json()), 1)

    def test_queryset_returns_multiple_calls_when_in_db(self):
        """Test that queryset returns all calls if there are many in db."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        calls = self.client.get('/api/calls/')
        self.assertEqual(len(calls.json()), 0)
        jabba = Contact(name="Jabba", number="+12068675309")
        jabba.save()
        call1 = Call(contact=jabba, direction="outgoing", status="completed")
        call1.save()
        han = Contact(name="Han", number="+15555555555")
        han.save()
        call2 = Call(contact=han, direction="incoming", status="busy")
        call2.save()
        nerfherder = Contact(name="Nerf Herder", number="+16666666666")
        nerfherder.save()
        call3 = Call(contact=nerfherder, direction="outgoing", status="completed")
        call3.save()
        calls = self.client.get('/api/calls/')
        self.assertEqual(len(calls.json()), 3)

    def test_text_queryset_returns_text_body_on_page(self):
        """Test that a call to the text api contains actually body content."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        text1 = Text(body="Jabba no watta.", sender="them")
        text1.save()
        text2 = Text(body="I'm telling you, Jabba, I can get the money.")
        text2.save()
        text3 = Text(body="Solo! Solo! Too Nakma Noya Solo!", sender="them")
        text3.save()
        texts = self.client.get('/api/texts/')
        self.assertTrue("Jabba no watta" in texts.content.decode())
        self.assertTrue("I'm telling you, Jabba, I can get the money." in texts.content.decode())
        self.assertTrue("Solo! Solo! Too Nakma Noya Solo!" in texts.content.decode())

    def test_text_queryset_returns_sender_attribute_in_json(self):
        """Test that a call to the text api contains the sender attribute."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        text1 = Text(body="Jabba no watta.", sender="them")
        text1.save()
        texts = self.client.get('/api/texts/')
        self.assertTrue("sender" in texts.content.decode())
        self.assertTrue("them" in texts.content.decode())

    def test_contact_queryset_returns_contact_attributes_in_json(self):
        """Test that a call to the contact api contains contact attributes."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        jabba = Contact(name="Jabba", number="+2068675309")
        jabba.save()
        contacts = self.client.get('/api/contacts/list/')
        self.assertTrue("+2068675309" in contacts.content.decode())
        self.assertTrue("Jabba" in contacts.content.decode())

    def test_call_queryset_returns_call_attributes_in_json(self):
        """Test that a call to the calls api contains call attributes."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        jabba = Contact(name="Jabba", number="+12068675309")
        jabba.save()
        call1 = Call(contact=jabba, direction="outgoing", status="completed")
        call1.save()
        calls = self.client.get('/api/calls/')
        self.assertTrue("direction" in calls.content.decode())
        self.assertTrue("outgoing" in calls.content.decode())
        self.assertTrue("time" in calls.content.decode())
        self.assertTrue("status" in calls.content.decode())
        self.assertTrue("contact" in calls.content.decode())

    def test_last_text_view_returns_latest_incoming_text(self):
        """LastText should return latest incoming text."""
        view = LastText.as_view()
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        text1 = Text(body="Jabba no watta.", sender="them")
        text1.save()
        request = self.request.get('/sf')
        request.user = user1
        response = view(request)
        self.assertIn('Jabba no watta', response.rendered_content.decode())
        text2 = Text(body="this shouldn't show up.", sender="you")
        text2.save()
        response = view(request)
        self.assertIn('Jabba no watta', response.rendered_content.decode())
        text3 = Text(body="Not the same.", sender="them")
        text3.save()
        response = view(request)
        self.assertIn('Not the same', response.rendered_content.decode())

    def test_get_contact_by_number_returns_right_contact(self):
        """Should return contact with given number."""
        view = GetContactByNumber.as_view()
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        request = self.request.get('/sf', number='1')
        request.user = user1
        jabba = Contact(name="Jabba the Hutt", number="+2068675309")
        jabba.save()
        response = view(request, number=2068675309)
        self.assertIn('Jabba the Hutt', response.rendered_content.decode())
