from django.views.generic import ListView
from texts.models import Text
from django.http import HttpResponse
from django.views.generic import View
from braces.views import CsrfExemptMixin

from texts.forms import TextForm
from django.views.generic.edit import ModelFormMixin
from contacts.models import Contact
import os
from twilio.rest import TwilioRestClient


class ProcessHookView(CsrfExemptMixin, View):
    """Processing request from Twilio."""

    def post(self, request, *kwargs):
        """Process post requests from twilio."""
        body = decode_request_body(request.body)
        print("from: {}, message: {}".format(body["From"][0], body["Body"][0]))
        contact = Contact.objects.filter(number=body["From"][0]).first()
        if not contact:
            contact = Contact(number=body["From"][0])
            contact.save()
        if contact.number != os.environ["TWILIO_NUMBER"]:
            sender = "them"
        else:
            sender = "you"
        text = Text(sender=sender, contact=contact, body=body["Body"][0])
        text.save()
        return HttpResponse()


def decode_request_body(string):
    """Helper function to decode wsgi_request."""
    body = {}
    body_list = string.decode("utf-8").split('&')
    for i in body_list:
        body.setdefault(i.split("=")[0], []).append(i.split("=")[1])

    body["From"][0] = "+" + body["From"][0][3:]
    body["Body"][0] = body["Body"][0].replace("+", " ")
    return body


class TextView(ListView, ModelFormMixin):
    """A view for the texts."""

    model = Text
    form_class = TextForm

    template_name = "texts/texting.html"
    context_object_name = "texts"

    def get_queryset(self):
        # import pdb; pdb.set_trace()
        contact = Contact.objects.get(pk=self.kwargs.get('pk'))
        contacts_msgs = contact.texts
        last_ten = contacts_msgs.order_by('-id')[:10][::-1]
        return last_ten

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        # Explicitly states what get to call:
        return ListView.get(self, request, *args, **kwargs)

    def form_valid(self, form):
        """Execute if form is valid."""
        self.object = self.get_object()
        text = form.save()
        text.sender = 'you'
        text.save()

    def post(self, request, *args, **kwargs):
        # When the form is submitted, it will enter here
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


class MessageListView(ListView):
    """View to show all text message conversations."""
    template_name = 'texts/message_list.html'
    context_object_name = "contacts"
    model = Contact
