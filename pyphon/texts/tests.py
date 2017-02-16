from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse_lazy
import factory

from texts.models import Text
from texts.views import TextView, ProcessHookView, MessageListView
from texts.forms import NewTextForm

from contacts.models import Contact
from contacts.tests import ContactFactory

from bs4 import BeautifulSoup as Soup
import datetime


class TextFactory(factory.django.DjangoModelFactory):
    """Create  a text to test with."""

    class Meta:
        model = Text
    body = "It's a me, a Mario"
    sender = "you"


class TextTestCase(TestCase):
    """The Text app test runner."""

    def setUp(self):
        """Text test setup."""
        self.client = Client()
        self.request = RequestFactory()
        self.contacts = [ContactFactory.create() for i in range(20)]

    def add_text_to_contact(self, contact):
        """Give the contact a text."""
        text = TextFactory.create()
        text.contact = contact
        text.save()

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
        self.assertTrue(isinstance(Text.objects.first().time, datetime.datetime))

    def test_text_repr_is_body(self):
        """Test that texts are properly represented."""
        text1 = Text(body="No bata tu tu, muni, muni.", sender="them")
        text1.save()
        self.assertTrue(text1.__str__() == text1.body[:20])

    # def test_text_view_returns_first_text(self):
    #     """Test that text view returns a text."""
    #     text1 = Text(body="Jabba no watta.", sender="them", contact=self.contacts[0])
    #     text1.save()
    #     text2 = Text(body="Too Nakma Noya Solo!", sender="you", contact=self.contacts[0])
    #     text2.save()
    #     response = self.client.get(reverse_lazy('texts', kwargs={"pk": self.contacts[0].id}))
    #     self.assertIn(text1.body, response.content.decode("utf-8"))

    # def test_text_view_returns_second_text(self):
    #     """Test that text view returns two texts."""
    #     text1 = Text(body="Jabba no watta.", sender="them", contact=self.contacts[0])
    #     text1.save()
    #     text2 = Text(body="Too Nakma Noya Solo!", sender="you", contact=self.contacts[0])
    #     text2.save()
    #     response = self.client.get(reverse_lazy('texts', kwargs={"pk": self.contacts[0].id}))
    #     self.assertIn(text2.body, response.content.decode("utf-8"))

    def test_text_view_status_200(self):
        """Test that text view returns ok status."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        text1 = Text(body="Jabba no watta.", sender="them", contact=self.contacts[0])
        text1.save()
        response = self.client.get(reverse_lazy('texts', kwargs={"pk": self.contacts[0].id}))
        self.assertTrue(response.status_code == 200)

    def test_text_view_template(self):
        """Test that text view uses texts template."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        text1 = Text(body="Jabba no watta.", sender="them", contact=self.contacts[0])
        text1.save()
        response = self.client.get(reverse_lazy('texts', kwargs={"pk": self.contacts[0].id}))
        self.assertTemplateUsed(response, 'texts/texting.html')

# Needs tests that use self.client and bs4 to count texts on page

    def create_new_contact(self):
        """Create a contact for testing."""
        jabba = Contact(number='+15005550006')
        jabba.save()
        return jabba.id

    def submit_new_text_form(self):
        """Submit a new text form."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
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
            'Body': 'ToCountry=US&ToState=&FromCity=SEATTLE&Body=Test&FromCountry=US&To=%2B1222222222&From=%2B11111111111&ApiVersion=2010-04-01'})
        contacts = Contact.objects.count()
        self.assertGreater(contacts, old_contacts)

    def test_no_contact_is_added_when_text_from_contact_received(self):
        """Test that no new contact is added when receiving text from known number."""
        new_contact = Contact()
        new_contact.number = "+11111111111"
        new_contact.name = "test"
        new_contact.save()
        contact_count = Contact.objects.count()
        self.client.post(reverse_lazy('text_hook'), {
            'Body': 'ToCountry=US&ToState=&FromCity=SEATTLE&Body=Test&FromCountry=US&To=%2B1222222222&From=%2B11111111111&ApiVersion=2010-04-01'})
        self.assertEqual(contact_count, Contact.objects.count())

    def test_new_text_in_db_when_received(self):
        """Test that a new text will appear in the database when it's received."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        self.client.post(reverse_lazy('text_hook'), {
            'Body': 'ToCountry=US&ToState=&FromCity=SEATTLE&Body=Test&FromCountry=US&To=%2B1222222222&From=%2B11111111111&ApiVersion=2010-04-01'})
        self.assertEqual(Text.objects.count(), 1)

    def test_new_text_in_db_has_correct_info(self):
        """Test that a new text is added in the database with correct info."""
        self.client.post(reverse_lazy('text_hook'), {
            'Body': 'ToCountry=US&ToState=&FromCity=SEATTLE&Body=Test&FromCountry=US&To=%2B1222222222&From=%2B11111111111&ApiVersion=2010-04-01'})
        text = Text.objects.first()
        self.assertTrue(text.body == "Test")

    def test_new_text_has_correct_contact_when_contact_exists(self):
        """Test that incoming test gets matched to correct contact if contact already exists."""
        new_contact = Contact()
        new_contact.number = "+11111111111"
        new_contact.name = "test"
        new_contact.save()
        self.client.post(reverse_lazy('text_hook'), {
            'Body': 'ToCountry=US&ToState=&FromCity=SEATTLE&Body=Test&FromCountry=US&To=%2B1222222222&From=%2B11111111111&ApiVersion=2010-04-01'})
        text = Text.objects.first()
        self.assertEqual(text.contact, new_contact)

    def test_new_contact_has_empty_string_when_new_text(self):
        """Test that a new text from a new contact will create a contact with empty string as name."""
        self.client.post(reverse_lazy('text_hook'), {
            'Body': 'ToCountry=US&ToState=&FromCity=SEATTLE&Body=Test&FromCountry=US&To=%2B1222222222&From=%2B11111111111&ApiVersion=2010-04-01'})
        contact = Contact.objects.last()
        self.assertEqual(contact.name, "")

    def test_message_list_view_client(self):
        """Test that contact list view returns a response from the same client."""
        ContactFactory.create(name="Bob Barker", number="+15555555555")
        response = self.client.get(reverse_lazy("message_list"))
        self.assertEqual(response.client, self.client)

    def test_message_list_view_status(self):
        """Test that contact list view returns 200 OK response."""
        user1 = User()
        user1.save()
        view = MessageListView.as_view()
        req = self.request.get(reverse_lazy("message_list"))
        req.user = user1
        response = view(req)
        self.assertEqual(response.status_code, 200)

    def test_message_list_view_content_name(self):
        """Test that contact list view returns the contact's name in the body."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        contact = ContactFactory.create(name="Bob Barker", number="+15555555555")
        text = TextFactory.create()
        text.contact = contact
        text.save()
        response = self.client.get(reverse_lazy("message_list"))
        self.assertIn(contact.name, response.content.decode("utf-8"))

    def test_message_list_view_content_title(self):
        """Test that contact list view returns 'Message List' as the title of the body."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        ContactFactory.create(name="Bob Barker", number="+15555555555")
        response = self.client.get(reverse_lazy("message_list"))
        self.assertTemplateUsed(response, "texts/message_list.html")

    def test_message_list_view_returns_first_contact(self):
        """Test that contact list view returns name of first contact."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        self.add_text_to_contact(self.contacts[0])
        response = self.client.get(reverse_lazy("message_list"))
        self.assertIn(self.contacts[0].name, response.content.decode("utf-8"))

    def test_message_list_view_returns_middle_contact(self):
        """Test that contact list view returns name of 10th contact."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        self.add_text_to_contact(self.contacts[10])
        response = self.client.get(reverse_lazy("message_list"))
        self.assertIn(self.contacts[10].name, response.content.decode("utf-8"))

    def test_message_list_view_returns_last_contact(self):
        """Test that contact list view returns name of last contact."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        self.add_text_to_contact(self.contacts[-1])
        response = self.client.get(reverse_lazy("message_list"))
        self.assertIn(self.contacts[-1].name, response.content.decode("utf-8"))

    def test_message_list_view_has_correct_number_of_contacts(self):
        """Test that contact list view has the same number of entries as contacts."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        [self.add_text_to_contact(contact) for contact in self.contacts]
        response = self.client.get(reverse_lazy("message_list"))
        soup = Soup(response.content, 'html.parser')
        self.assertEqual(len(soup.find_all('tr', class_="contact")),
                         len(self.contacts))


class NewTextTestCase(TestCase):
    """The Text app test runner."""

    def setUp(self):
        """Text test setup."""
        self.client = Client()
        self.request = RequestFactory()

    def test_new_text_view_status_200(self):
        """Test that new text view returns ok status."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        response = self.client.get(reverse_lazy('new'))
        self.assertTrue(response.status_code == 200)

    def test_new_text_number_input_form(self):
        """Test that the form saves the number from the input field."""
        form_data = {'number': '2065555555'}
        form = NewTextForm(data=form_data)
        self.assertEqual(form.data['number'], '2065555555')

    def test_new_number_saves_as_new_contact(self):
        """Test that the form saves the number as a contact."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        self.client.post(reverse_lazy('new'), {'number': "11111111111"})
        contact = Contact.objects.first()
        self.assertEqual(contact.number, "+11111111111")

    def test_new_text_redirects_on_success(self):
        """Test that creating a new contact successfully redirects."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        jabba = Contact(name="Jabba", number="+9999999999")
        jabba.save()
        response = self.client.post(reverse_lazy('new'), {'number': "9999999999"})
        self.assertTrue(response.status_code == 302)

    def test_new_text_number_isalpha_refreshes_with_error_msg(self):
        """Test that if you enter a non phone number, you refresh page."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        response = self.client.post(reverse_lazy('new'), {'number': "hello"})
        self.assertTrue('<li>Enter a valid phone number.</li>' in response.content.decode())
