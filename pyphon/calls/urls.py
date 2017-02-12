from django.conf.urls import url
from calls.views import call_view

urlpatterns = [
    url(r'^$', call_view, name="calls"),
]
