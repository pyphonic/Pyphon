from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import TextViewSet, CallViewSet, ContactViewSet, LastText

urlpatterns = [
    url(r'^texts/$', TextViewSet.as_view({'get': 'list'}), name='api_texts'),
    url(r'^texts/last/$', LastText.as_view(), name='api_texts_retrieve'),
    url(r'^calls/$', CallViewSet.as_view({'get': 'list'}), name='api_calls'),
    url(r'^contacts/list/$', ContactViewSet.as_view({'get': 'list'}), name='api_contacts_list'),
    url(r'^contacts/retrieve/(?P<number>\d+)/$', ContactViewSet.as_view({'get': 'retrieve'}), name='api_contacts_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
