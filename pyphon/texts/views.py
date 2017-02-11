from django.shortcuts import render
from texts.models import Text


def text_view(request):
    """Send and receive text messages."""
    texts = Text.objects.all()
    return render(request, "texts/texting.html", {
        'texts': texts})
