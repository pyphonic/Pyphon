from django.conf.urls import url
from texts.views import text_view, ProcessHookView

urlpatterns = [
    url(r'^$', text_view, name="texts"),
    url(r'^hook/', ProcessHookView.as_view(), name="text_hook")
]
