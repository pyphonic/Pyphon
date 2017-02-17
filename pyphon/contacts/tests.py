from django.test import TestCase, Client, RequestFactory
from contacts.models import Contact
from contacts.views import ContactIdView, ContactAddView, ContactEditView, ContactListView, validate_number
import factory
from django.db.utils import IntegrityError
import random
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User

# Create your tests here.
rand = random.Random()


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact
    name = factory.Sequence(lambda n: "Name {}".format(n))
    number = factory.Sequence(lambda n: "+1" + str(rand.randint(1000000000, 9999999999)))


class ContactTestCase(TestCase):

    def setUp(self):
        """User setup for tests."""
        self.client = Client()
        self.request = RequestFactory()

    def test_no_initial_contacts(self):
        """Test that there are no contacts in the contact list before they are added."""
        self.assertEqual(Contact.objects.count(), 0)

    def test_contacts_are_added(self):
        """Test that the length of the contacts increases as they are created."""
        self.contacts = [ContactFactory.create() for i in range(10)]
        self.assertEqual(Contact.objects.count(), 10)

    def test_create_contact_number_only(self):
        """Test that when a contact is created, it gives a default name of an empty string."""
        contact = Contact()
        self.assertEqual(contact.name, "")

    def test_create_contact_with_name(self):
        """Test that when a contact is created, it has the specified name and phone number."""
        contact = Contact(name="Bob Barker", number="+15555555555")
        self.assertEqual((contact.name, contact.number), ("Bob Barker", "+15555555555"))

    def test_create_multiple_contacts_same_number(self):
        """Test that when multiple contacts are created with the same number, they replace each other."""
        contact1 = Contact(name="Bob Barker", number="+15555555555")
        contact1.save()
        contact2 = Contact(name="Jim Henson", number="+15555555555")
        self.assertRaises(IntegrityError, contact2.save)

    def test_create_multiple_contacts_different_number(self):
        """Test create two contacts with different numbers increases count of contact.objects.count()"""
        contact1 = ContactFactory.create(name="Bob Barker", number="+15555555555")
        contact2 = ContactFactory.create(name="Jin Henson", number="+14444444444")
        self.assertEqual(Contact.objects.count(), 2)

    def test_create_multiple_contacts_same_name(self):
        """Test create two contacts with the same name but different number increases count of contact.objects.count(), no error."""
        contact1 = ContactFactory.create(name="Bob Barker", number="+15555555555")
        contact2 = ContactFactory.create(name="Bob Barker", number="+14444444444")
        self.assertEqual(Contact.objects.count(), 2)

    def test_update_contact(self):
        """Test that a contact has new information after it gets updated."""
        contact1 = ContactFactory.create(name="Bob Barker", number="+15555555555")
        contact1.name = "Jim Henson"
        contact1.number = "+14444444444"
        contact1.save()
        self.assertEqual((Contact.objects.first().name, Contact.objects.first().number), ("Jim Henson", "+14444444444"))

    def test_contact_string_method_no_name(self):
        """Test that contact's __str__() method returns the number if no name is given."""
        contact = ContactFactory.create(name="", number="+15555555555")
        self.assertEqual(str(contact), "(555) 555-5555")

    def test_contact_string_method_with_name(self):
        """Test that contact's __str__() method returns the name if it has one."""
        contact = ContactFactory.create(name="Bob Barker", number="+15555555555")
        self.assertEqual(str(contact), "Bob Barker")

    def test_contact_id_view_client(self):
        """Test that contact id view returns a response from the same client."""
        contact = ContactFactory.create(name="Bob Barker", number="+15555555555")
        response = self.client.get(reverse_lazy("contact_detail", kwargs={"pk": contact.id}))
        self.assertEqual(response.client, self.client)

    def test_contact_id_view_status(self):
        """Test that contact id view returns 200 OK response."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        contact = ContactFactory.create(name="Bob Barker", number="+15555555555")
        response = self.client.get(reverse_lazy("contact_detail", kwargs={"pk": contact.id}))
        self.assertEqual(response.status_code, 200)

    def test_contact_id_view_content_name(self):
        """Test that contact id view returns the contact's name in the body."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        contact = ContactFactory.create(name="Bob Barker", number="+15555555555")
        response = self.client.get(reverse_lazy("contact_detail", kwargs={"pk": contact.id}))
        self.assertIn(contact.name, response.content.decode("utf-8"))

    def test_contact_id_view_content_number(self):
        """Test that contact id view returns the contact's number in the body."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        contact = ContactFactory.create(name="", number="+15555555555")
        response = self.client.get(reverse_lazy("contact_detail", kwargs={"pk": contact.id}))
        self.assertIn('(555) 555-5555', response.content.decode("utf-8"))

    def test_contact_id_view_contact_returned(self):
        """Test that contact id view returns the contact in the context."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        contact = ContactFactory.create(name="Bob Barker", number="+15555555555")
        view = ContactIdView.as_view()
        request = self.request.get(reverse_lazy("contact_detail", kwargs={"pk": contact.id}))
        request.user = user1
        response = view(request, pk=contact.id)
        self.assertTrue(response.context_data['contact'])

    def test_contact_id_view_returns_contact_name(self):
        """Test that contact id view returns the contact in the context."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        contact = ContactFactory.create(name="Max Rebo", number="+15555555555")
        view = ContactIdView.as_view()
        request = self.request.get(reverse_lazy("contact_detail", kwargs={"pk": contact.id}))
        request.user = user1
        response = view(request, pk=contact.id)
        self.assertTrue(response.context_data['contact'].name == "Max Rebo")

    def test_contact_id_content_detail_template_used(self):
        """Test that contact id view uses the right template."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        contact = ContactFactory.create(name="Bob Barker", number="+15555555555")
        response = self.client.get(reverse_lazy("contact_detail", kwargs={"pk": contact.id}))
        self.assertTemplateUsed(response, "contacts/contact_detail.html")

    def test_contact_id_view_edit_link(self):
        """Test that contact id view has a link to edit contact."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        contact = ContactFactory.create(name="Zero", number="+15555555555")
        response = self.client.get(reverse_lazy("contact_detail", kwargs={"pk": contact.id}))
        self.assertIn('href="edit/"', response.content.decode("utf-8"))

    def test_contact_id_view_text_link(self):
        """Test that contact id view has a link to text the contact."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        contact = ContactFactory.create(name="Jabba", number="+15555555555")
        response = self.client.get(reverse_lazy("contact_detail", kwargs={"pk": contact.id}))
        self.assertIn('href="/texts/contact/' + str(contact.id) + '/"', response.content.decode("utf-8"))

    def test_contact_edit_view_client(self):
        """Test that contact edit view returns a response from the same client."""
        contact = ContactFactory.create(name="Bob Barker", number="+15555555555")
        response = self.client.get(reverse_lazy("edit_contact", kwargs={"pk": contact.id}))
        self.assertEqual(response.client, self.client)

    def test_contact_edit_view_status(self):
        """Test that contact edit view returns 200 OK response."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        contact = ContactFactory.create(name="Bob Barker", number="+15555555555")
        response = self.client.get(reverse_lazy("edit_contact", kwargs={"pk": contact.id}))
        self.assertEqual(response.status_code, 200)

    def test_contact_edit_view_content_name(self):
        """Test that contact edit view returns the contact's name in the body."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        contact = ContactFactory.create(name="Bob Barker", number="+15555555555")
        response = self.client.get(reverse_lazy("edit_contact", kwargs={"pk": contact.id}))
        self.assertIn(contact.name, response.content.decode("utf-8"))

    def test_contact_edit_view_content_title(self):
        """Test that contact edit view returns the contact's name in the body."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        contact = ContactFactory.create(name="Bob Barker", number="+15555555555")
        response = self.client.get(reverse_lazy("edit_contact", kwargs={"pk": contact.id}))
        self.assertTemplateUsed(response, "contacts/edit_contact.html")

    # def test_contact_edit_view_

    def test_contact_add_view_client(self):
        """Test that contact add view returns a response from the same client."""
        ContactFactory.create(name="Bob Barker", number="+15555555555")
        response = self.client.get(reverse_lazy("new_contact"))
        self.assertEqual(response.client, self.client)

    def test_contact_add_view_status(self):
        """Test that contact add view returns 200 OK response."""
        user1 = User()
        user1.save()
        view = ContactAddView.as_view()
        req = self.request.get(reverse_lazy("new_contact"))
        req.user = user1
        response = view(req)
        self.assertEqual(response.status_code, 200)

    def test_contact_add_view_content_title(self):
        """Test that contact add view returns 'new contact' in the body."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        response = self.client.get(reverse_lazy("new_contact"))
        self.assertTemplateUsed(response, "contacts/new_contact.html")

    def test_contact_list_view_client(self):
        """Test that contact list view returns a response from the same client."""
        ContactFactory.create(name="Bob Barker", number="+15555555555")
        response = self.client.get(reverse_lazy("contacts"))
        self.assertEqual(response.client, self.client)

    def test_contact_list_view_status(self):
        """Test that contact list view returns 200 OK response."""
        user1 = User()
        user1.save()
        view = ContactListView.as_view()
        req = self.request.get(reverse_lazy("contacts"))
        req.user = user1
        response = view(req)
        self.assertEqual(response.status_code, 200)

    def test_contact_list_view_content_name(self):
        """Test that contact list view returns the contact's name in the body."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        contact = ContactFactory.create(name="Bob Barker", number="+15555555555")
        response = self.client.get(reverse_lazy("contacts"))
        self.assertIn(contact.name, response.content.decode("utf-8"))

    def test_contact_list_view_content_number(self):
        """Test that contact list view doesn't return the contact in the body."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        contact = ContactFactory.create(name="", number="+15555555555")
        response = self.client.get(reverse_lazy("contacts"))
        self.assertNotIn(str(contact.number), response.content.decode("utf-8"))

    def test_contact_list_view_returns_contact(self):
        """Test that contact list view returns 200 OK response."""
        user1 = User()
        user1.save()
        jabba = Contact(name="Jabba", number="+1234567890")
        jabba.save()
        view = ContactListView.as_view()
        req = self.request.get(reverse_lazy("contacts"))
        req.user = user1
        contacts = Contact.objects.all()
        response = view(req, {"contacts": contacts})
        contact = response.context_data['contacts'][0]
        self.assertTrue(contact.name == "Jabba")

    def test_contact_list_view_returns_two_contacts(self):
        """Test that contact list view returns 200 OK response."""
        user1 = User()
        user1.save()
        jabba = Contact(name="Jabba", number="+1234567890")
        jabba.save()
        zero = Contact(name="Zero", number="+1234567840")
        zero.save()
        view = ContactListView.as_view()
        req = self.request.get(reverse_lazy("contacts"))
        req.user = user1
        contacts = Contact.objects.all()
        response = view(req, {"contacts": contacts})
        all_contacts = response.context_data['contacts']
        self.assertTrue(len(all_contacts) == 2)

    def test_contact_list_template_used(self):
        """Test that contact list view uses the right template."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        contact = ContactFactory.create(name="Bob Barker", number="+15555555555")
        response = self.client.get(reverse_lazy("contacts"))
        self.assertTemplateUsed(response, "contacts/contacts_list.html")

    def test_contact_list_view_returns_id_view_link(self):
        """Test that contact list view has link to id view."""
        user1 = User()
        user1.save()
        self.client.force_login(user1)
        zero = Contact(name="Zero", number="+1234567840")
        zero.save()
        response = self.client.get(reverse_lazy("contacts"))
        self.assertIn('href="/contacts/' + str(zero.id) + '/"', response.content.decode("utf-8"))

    def test_validate_number_no_change(self):
        """Test that an already valid number returns unchanged."""
        number = "+12345678901"
        self.assertEqual(validate_number(number)[0], number)

    def test_validate_number_no_change_modified(self):
        """Test that an already valid number returns true for modified."""
        number = "+12345678901"
        self.assertNotEqual(validate_number(number)[1], True)

    def test_validate_number_no_plus(self):
        """Test that an already valid number returns unchanged."""
        number = "12345678901"
        self.assertEqual(validate_number(number)[0], "+12345678901")

    def test_validate_number_no_plus_modified(self):
        """Test that an already valid number returns true for modified."""
        number = "12345678901"
        self.assertEqual(validate_number(number)[1], True)

    def test_validate_number_no_plus_one(self):
        """Test that an already valid number returns unchanged."""
        number = "2345678901"
        self.assertEqual(validate_number(number)[0], "+12345678901")

    def test_validate_number_no_plus_one_modified(self):
        """Test that an already valid number returns true for modified."""
        number = "2345678901"
        self.assertEqual(validate_number(number)[1], True)