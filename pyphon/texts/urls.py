from django.conf.urls import url
from texts.views import TextView

urlpatterns = [
    # url(r'^(?P<pk>\d+)/$', TextView.as_view(), name="texts"),
    # url(r'^$', MessageListView.as_view(), name="message_list"),
    url(r'^$', TextView.as_view(), name="texts"),

]
