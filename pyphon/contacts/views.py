from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from contacts.models import Contact


# Create your views here.
class ContactIdView(LoginRequiredMixin, DetailView):
    """View for individual contacts."""

    login_url = '/login/'
    template_name = "contacts/contact_detail.html"
    model = Contact


class ContactListView(LoginRequiredMixin, ListView):
    """View to list all contacts."""

    login_url = '/login/'
    template_name = "contacts/contacts_list.html"
    model = Contact
    context_object_name = 'contacts'
    queryset = Contact.objects.exclude(name__isnull=True).exclude(name__exact='').order_by('name')

class ContactAddView(LoginRequiredMixin, CreateView):
    """View to create a new contact."""

    login_url = '/login/'
    template_name = "contacts/new_contact.html"
    model = Contact
    fields = ['name', 'number']
    context_object_name = 'contact'
    success_url = '/contacts/'


class ContactEditView(LoginRequiredMixin, UpdateView):
    """View to create a new contact."""

    login_url = '/login/'
    template_name = "contacts/edit_contact.html"
    model = Contact
    fields = ['name', 'number']
    context_object_name = 'contact'
    success_url = '/contacts/'
