from django.conf.urls import url
from texts.views import TextView, ProcessHookView

urlpatterns = [
    url(r'^$', TextView.as_view(), name="texts"),
    url(r'^hook/', ProcessHookView.as_view(), name="text_hook")
]
