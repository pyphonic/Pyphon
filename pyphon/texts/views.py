from django.shortcuts import render
from texts.models import Text
from django.http import HttpResponse
from django.views.generic import View
from braces.views import CsrfExemptMixin


def text_view(request):
    """Send and receive text messages."""
    texts = Text.objects.all()
    return render(request, "texts/texting.html", {
        'texts': texts})


class ProcessHookView(CsrfExemptMixin, View):
    """Processing request from Twilio."""

    def post(self, request, *kwargs):
        """Process post requests from twilio."""
        body = decode_request_body(request.body)
        print("from: {}, message: {}".format(body["From"][0], body["Body"][0]))
        return HttpResponse()


def decode_request_body(string):
    """Helper function to decode wsgi_request."""
    body = {}
    body_list = string.decode("utf-8").split('&')
    for i in body_list:
        body.setdefault(i.split("=")[0], []).append(i.split("=")[1])

        body["From"][0] = body["From"][0][3:]
        body["Body"][0] = body["Body"][0].replace("+", " ")
    return body
