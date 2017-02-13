"""Views for Pyphon base app."""

from django.shortcuts import render
from django.conf import settings
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from twilio import twiml
from twilio.util import TwilioCapability
from twilio.rest import TwilioRestClient


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
    print('in call method')

    if request.POST.get('Caller', '') == settings.TWILIO_NUMBER:
        print('outgoing')
        with response.dial(callerId=settings.TWILIO_NUMBER) as r:
            """If the browser sent a phoneNumber param, we know this request
            is an outgoing call from the pyphone"""
            if 'phoneNumber' in request.POST:
                r.number(request.POST['phoneNumber'])
    else:
        """Otherwise we assume this request is an incoming call"""
        print('incoming')
        with response.dial() as r:
            r.client('caller')

    return HttpResponse(str(response))


def answered(request):
    """Hang up the call."""
    return render(request, "calls/answered.html", {})
