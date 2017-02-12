from django.conf.urls import url
from texts.views import TextView

urlpatterns = [
    url(r'^$', TextView.as_view(), name="texts"),
]
