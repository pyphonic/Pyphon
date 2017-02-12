from django.shortcuts import render
from django.views.generic import ListView
from texts.models import Text


class TextView(ListView):
    """A view for the texts."""
    template_name = "texts/texting.html"
    context_object_name = "texts"
    model = Text
