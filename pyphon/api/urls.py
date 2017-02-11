from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import TextViewSet

urlpatterns = [
    url(r'^texts/$', TextViewSet.as_view({'get': 'list'}), name='api_texts'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
