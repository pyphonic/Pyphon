from django.conf.urls import url
<<<<<<< HEAD
from texts.views import text_view, ProcessHookView

urlpatterns = [
    url(r'^$', text_view, name="texts"),
    url(r'^hook/', ProcessHookView.as_view(), name="text_hook")
=======
from texts.views import TextView

urlpatterns = [
    url(r'^$', TextView.as_view(), name="texts"),
>>>>>>> a6c73da2d5650edd2d88a462ba58ff1c219ef0a1
]
