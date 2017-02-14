from django.conf.urls import url
from calls.views import callview, get_token, call

urlpatterns = [
    url(r'^$', callview, name="calls"),
    url(r'^token$', get_token, name='token'),
    url(r'^call$', call, name='call'),
]
