"""Views for Pyphon base app."""

from django.conf import settings
from django.views.generic import TemplateView
from braces.views import CsrfExemptMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from texts.models import Text


class HomeView(CsrfExemptMixin, TemplateView):
    """A class based view for home page."""
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = "pyphon/home.html"
