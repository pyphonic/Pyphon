"""Views for Pyphon base app."""

from django.conf import settings
from django.views.generic import TemplateView

from texts.models import Text


class HomeView(TemplateView):
    """A class based view for home page."""

    template_name = "pyphon/home.html"
