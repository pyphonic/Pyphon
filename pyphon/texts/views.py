from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import View, ListView, CreateView
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.parsers import FormParser

from braces.views import CsrfExemptMixin

from twilio.rest import TwilioRestClient

from contacts.models import Contact
from texts.models import Text
from texts.forms import TextForm, NewTextForm

import os


class ProcessHookView(CsrfExemptMixin, View):
    """Processing request from Twilio."""

    def post(self, request, *kwargs):
        parser = FormParser()
        query_dict = parser.parse(request)
        contact = Contact.objects.filter(number=query_dict["From"]).first()
        if not contact:
            contact = Contact(number=query_dict["From"])
            contact.save()
        if contact.number != os.environ["TWILIO_NUMBER"]:
            sender = "them"
        else:
            sender = "you"
        text = Text(sender=sender, contact=contact, body=query_dict["Body"])
        text.save()
        return HttpResponse()


class TextView(LoginRequiredMixin, CreateView):
    """A view for the texts."""

    login_url = '/login/'
    model = Text
    form_class = TextForm
    template_name = "texts/texting.html"

    def get_context_data(self, **kwargs):
        ctx = super(TextView, self).get_context_data(**kwargs)
        ctx['contact'] = Contact.objects.get(pk=self.kwargs.get("pk"))
        # import pdb;pdb.set_trace()
        return ctx

    def form_valid(self, form):
        """Execute if form is valid."""
        self.object = self.get_object()
        text = form.save()
        text.sender = 'you'
        text.save()

    def post(self, request, *args, **kwargs):
        """Post response."""
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            # self.object = self.form.save()
            # Here ou may consider creating a new instance of form_class(),
            # so that the form will come clean.
            text = self.form.save()
            text.sender = 'you'
            text.contact = Contact.objects.get(pk=int(self.kwargs.get('pk')))
            account_sid = os.environ["ACCOUNT_SID"]
            auth_token = os.environ["AUTH_TOKEN"]
            twilio_number = os.environ["TWILIO_NUMBER"]
            client = TwilioRestClient(account_sid, auth_token)
            client.messages.create(
                to=str(text.contact.number),
                from_=twilio_number,
                body=text.body
            )
            text.save()
        # Whether the form validates or not, the view will be rendered by get()
        return self.get(request, *args, **kwargs)


class NewTextView(LoginRequiredMixin, CreateView):
    """View to create a new contact."""

    login_url = '/login/'
    model = Contact
    form_class = NewTextForm
    template_name = "texts/new_text.html"

    def form_valid(self, form):
        self.object = self.get_object()
        contact_form = form.save()
        print("in form_valid")
        contact_form.save()

    def post(self, request, *args, **kwargs):
        """Post response."""
        self.object = None
        self.form = self.get_form(self.form_class)

        if not self.form.is_valid():
            number = request.POST['number']
            number = "+" + number
            if Contact.objects.filter(number=number):
                contact = Contact.objects.filter(number=number).first()
            else:
                contact = Contact(number=number)
                contact.save()
            pk = contact.pk
            return redirect(reverse_lazy('contact_detail', kwargs={'pk': pk}))

        return self.get(request, *args, **kwargs)


class MessageListView(LoginRequiredMixin, ListView):
    """View to show all text message conversations."""

    login_url = '/login/'
    template_name = 'texts/message_list.html'
    context_object_name = "contacts"
    model = Contact

    def get_queryset(self):
        return Contact.objects.exclude(texts__isnull=True)
