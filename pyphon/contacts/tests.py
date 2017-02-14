from django.test import TestCase, Client, RequestFactory
from contacts.models import Contact
import factory
from django.db.utils import IntegrityError
import random

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


    # Test there is no contact at first
    def test_no_initial_contacts(self):
        """Test that there are no contacts in the contact list before they are added."""
        self.assertEqual(Contact.objects.count(), 0)

    # Test that contact's count increases as contacts are created
    def test_contacts_are_added(self):
        """Test that the length of the contacts increases as they are created."""
        self.contacts = [ContactFactory.create() for i in range(10)]
        self.assertEqual(Contact.objects.count(), 10)

    # Test create a contact with only a phone number -> name is ""
    def test_create_contact_number_only(self):
        """Test that when a contact is created, it gives a default name of an empty string."""
        contact = Contact()
        self.assertEqual(contact.name, "")

    # Test create a contact has right info
    def test_create_contact_with_name(self):
        """Test that when a contact is created, it has the specified name and phone number."""
        contact = Contact(name="Bob Barker", number="+15555555555")
        self.assertEqual((contact.name, contact.number), ("Bob Barker", "+15555555555"))

    # Test create two contacts with same number does not increase count of contact.objects.count()
    def test_create_multiple_contacts_same_number(self):
        """Test that when multiple contacts are created with the same number, they replace each other."""
        contact1 = Contact(name="Bob Barker", number="+15555555555")
        contact1.save()
        contact2 = Contact(name="Jim Henson", number="+15555555555")
        self.assertRaises(IntegrityError, contact2.save)

    # Test create two contacts with different numbers increases count of contact.objects.count()
    def test_create_multiple_contacts_different_number(self):
        contact1 = ContactFactory.create(name="Bob Barker", number="+15555555555")
        contact2 = ContactFactory.create(name="Jin Henson", number="+14444444444")
        self.assertEqual(Contact.objects.count(), 2)

    # Test update an existing contact
    def test_update_contact(self):
        """Test that a contact has new information after it gets updated."""
        contact1 = ContactFactory.create(name="Bob Barker", number="+15555555555")
        contact1.name = "Jim Henson"
        contact1.number = "+14444444444"
        contact1.save()
        self.assertEqual((Contact.objects.first().name, Contact.objects.first().number), ("Jim Henson", "+14444444444"))

    # Test contact __str__() method on contact without a name
    def test_contact_string_method_no_name(self):
        """Test that contact's __str__() method returns the number if no name is given."""
        contact = ContactFactory.create(name="", number="+15555555555")
        self.assertEqual(str(contact), "+15555555555")

    # Test contact __str__() method on contact with a NameError
    def test_contact_string_method_with_name(self):
        """Test that contact's __str__() method returns the name if it has one."""
        contact = ContactFactory.create(name="Bob Barker", number="+15555555555")
        self.assertEqual(str(contact), "Bob Barker")
