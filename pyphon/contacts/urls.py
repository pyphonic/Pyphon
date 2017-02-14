from django.conf.urls import url
from contacts.views import ContactIdView, ContactListView, ContactAddView

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', ContactIdView.as_view(), name="contact_detail"),
    url(r'^$', ContactListView.as_view(), name='contacts'),
    url(r'^new/$', ContactAddView.as_view(), name='new_contact'),
]
