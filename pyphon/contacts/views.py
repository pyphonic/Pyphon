from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.db.utils import IntegrityError

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

    def post(self, request, *args, **kwargs):
        """Post response."""
        self.form = self.get_form(self.form_class)
        number = request.POST['number']
        name = request.POST['name']
        number, modified = validate_number(number)

        if self.form.is_valid() or modified:
            if Contact.objects.filter(number=number):
                contact = Contact.objects.filter(number=number).first()
                contact.name = name
                contact.save()
            else:
                contact = Contact(name=name, number=number)
                contact.save()
            pk = contact.pk
            return redirect(reverse_lazy("contact_detail", kwargs={'pk': pk}))
        return self.get(request, *args, **kwargs)


class ContactEditView(LoginRequiredMixin, UpdateView):
    """View to create a new contact."""

    login_url = '/login/'
    template_name = "contacts/edit_contact.html"
    model = Contact
    fields = ['name', 'number']
    context_object_name = 'contact'
    success_url = '/contacts/'

    def post(self, request, *args, **kwargs):
        """Post response."""
        self.form = self.get_form(self.form_class)
        number = request.POST['number']
        number, modified = validate_number(number)

        if self.form.is_valid() or modified:
            contact = Contact.objects.filter(id=kwargs["pk"]).first()
            contact.name = request.POST['name']
            contact.number = number
            try:
                contact.save()
            except IntegrityError:
                return self.get(request, *args, **kwargs)
            pk = contact.pk
            return redirect(reverse_lazy("contact_detail", kwargs={'pk': pk}))
        return self.get(request, *args, **kwargs)


def validate_number(number):
    """Reformat number to be valid for the PhoneNumberField in the models."""
    modified = False
    number = number.replace("(", "").replace(")", "").replace("-", "").replace(" ", "").replace("+", "")
    if len(number) == 11 and number.isdigit() and not number[1] in "01":
        number = "+" + number
        modified = True
    elif len(number) == 10 and number.isdigit() and not number[0] in "01":
        number = "+1" + number
        modified = True
    return number, modified
