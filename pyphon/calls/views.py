"""Views for Pyphon base app."""

from django.shortcuts import render
from django.conf import settings
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from twilio import twiml
from twilio.util import TwilioCapability
from twilio.rest import TwilioRestClient


def callview(request):
    """A class based view for home page."""
    if request.POST:
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN

        capability = TwilioCapability(account_sid, auth_token)
        capability.allow_client_incoming("tommy")
        capability.allow_client_outgoing(settings.TWIML_APPLICATION_SID)
        print(capability.generate())

        client = TwilioRestClient(
            account_sid,
            auth_token)

        call = client.calls.create(
            url="http://demo.twilio.com/docs/voice.xml",
            to="+" + request.POST.get('numfield', ''),
            from_="+19493862388")
        print(call.sid)
    return render(request, "calls/dial_screen.html", {})


def get_token(request):
    """Returns a Twilio Client token"""
    # Create a TwilioCapability object with our Twilio API credentials
    capability = TwilioCapability(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN)
    # Allow our users to make outgoing calls with Twilio Client
    capability.allow_client_outgoing(settings.TWIML_APPLICATION_SID)

    # If the user is on the support dashboard page, we allow them to accept
    # incoming calls to "support_agent"
    # (in a real app we would also require the user to be authenticated)
    capability.allow_client_incoming('customer')

    # Generate the capability token
    token = capability.generate()

    return JsonResponse({'token': token})


@csrf_exempt
def call(request):
    """Returns TwiML instructions to Twilio's POST requests"""
    response = twiml.Response()

    with response.dial(callerId=settings.TWILIO_NUMBER) as r:
        # If the browser sent a phoneNumber param, we know this request
        # is a support agent trying to call a customer's phone
        if 'phoneNumber' in request.POST:
            r.number(request.POST['phoneNumber'])
        else:
            # Otherwise we assume this request is a customer trying
            # to contact support from the home page
            r.client('support_agent')

    return HttpResponse(str(response))
