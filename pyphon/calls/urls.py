from django.conf.urls import url
from calls.views import callview, get_token, call, CallListView

urlpatterns = [
    url(r'^dial$', callview, name="calls"),
    url(r'^token$', get_token, name='token'),
    url(r'^call$', call, name='call'),
    url(r'^$', CallListView.as_view(), name="call_list")
]
