from django.conf.urls import url
from texts.views import text_view

urlpatterns = [
    url(r'^$', text_view, name="texts"),
]
