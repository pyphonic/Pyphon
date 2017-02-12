from django.shortcuts import render
from texts.models import Text


def call_view(request):
    """Send and receive calls ."""
    texts = Text.objects.all()
    return render(request, "texts/texting.html", {
        'texts': texts})