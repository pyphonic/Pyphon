"""Views for Pyphon base app."""

from django.conf import settings
from django.views.generic import TemplateView
from braces.views import CsrfExemptMixin

from texts.models import Text


class HomeView(CsrfExemptMixin, TemplateView):
    """A class based view for home page."""

    template_name = "pyphon/home.html"
