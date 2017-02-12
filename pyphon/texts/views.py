import json

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
    def post(self, request, args, *kwargs):
        print(json.loads(request.body))
        return HttpResponse()
