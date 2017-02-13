from django.views.generic import ListView, CreateView, UpdateView, DetailView

from contacts.models import Contact


# Create your views here.
class ContactIdView(DetailView):
    """View for individual contacts."""

    template_name = "contacts/contact_detail.html"
    model = Contact


class ContactListView(ListView):
    """View to list all contacts."""

    template_name = "contacts/contacts_list.html"
    model = Contact
    context_object_name = 'contacts'


class ContactAddView(CreateView):
    """View to create a new contact."""

    template_name = "contacts/new_contact.html"
    model = Contact
    fields = ['name', 'number']
    context_object_name = 'contact'
    success_url = '/contacts/'
