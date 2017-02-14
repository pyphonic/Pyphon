"""Views for Pyphon base app."""

from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist
from twilio import twiml
from twilio.util import TwilioCapability
from twilio.rest import TwilioRestClient

from contacts.models import Contact
from calls.models import Call


@csrf_exempt
def callview(request):
    """A class based view for home page."""
    return render(request, "calls/dial_screen.html", {})


def get_token(request):
    """Returns a Twilio Client token
    Create a TwilioCapability object with our Twilio API credentials."""
    capability = TwilioCapability(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN)
    """Allow our users to make outgoing calls with Twilio Client"""
    capability.allow_client_outgoing(settings.TWIML_APPLICATION_SID)

    """Allow our users to accept incoming calls from pyphon"""
    capability.allow_client_incoming('caller')

    """Generate the capability token"""
    token = capability.generate()

    return JsonResponse({'token': token})


@csrf_exempt
def call(request):
    """Returns TwiML instructions to Twilio's POST requests"""

    response = twiml.Response()
    phone_number = request.POST.get('phoneNumber', '')

    if phone_number:
        """If the browser sent a phoneNumber param, we know this request
        is an outgoing call from the pyphone"""
        direction = 'outgoing'
        with response.dial(callerId=settings.TWILIO_NUMBER) as r:
            r.number(request.POST['phoneNumber'])
    else:
        """Otherwise we assume this request is an incoming call."""
        direction = 'incoming'
        with response.dial() as r:
            r.client('caller')
        phone_number = request.GET.get('From', '')

    try:
        contact = Contact.objects.get(number=phone_number)
    except ObjectDoesNotExist:
        contact = Contact(number=phone_number)
        contact.save()
    call = Call(
        contact=contact,
        direction=direction,
    )
    call.save()

    return HttpResponse(str(response))


class CallListView(ListView):
    """List view to show all past calls."""

    template_name = "calls/call_list.html"
    model = Call

    def get_context_data(self):
        """Return context data for call list view."""
        calls = Call.objects.all()
        # import pdb;pdb.set_trace()
        return {"calls": calls}
