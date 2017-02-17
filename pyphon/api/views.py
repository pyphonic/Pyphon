from texts.models import Text
from calls.models import Call
from contacts.models import Contact
from api.serializers import TextSerializer, CallSerializer, ContactSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets, permissions, views
from rest_framework.views import APIView

# from api.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response

from rest_framework_extensions.etag.mixins import ETAGMixin
from rest_framework_extensions.etag.decorators import etag


class TextViewSet(ETAGMixin, viewsets.ModelViewSet):

    serializer_class = TextSerializer

    def get_queryset(self):
        """Get queryset for photographer."""
        return Text.objects.all()


class CallViewSet(viewsets.ModelViewSet):

    serializer_class = CallSerializer

    def get_queryset(self):
        """Get queryset for photographer."""
        return Call.objects.all()


class ContactViewSet(viewsets.ModelViewSet):

    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


class LastText(APIView):
    """Retrieve most recent text."""

    def get_object(self):
        """Get latest incoming text."""
        return Text.objects.filter(sender='them').order_by('id').reverse()[0]

    def get(self, request, format=None):
        """Return json response representing latest text."""
        recent_text = self.get_object()
        serializer = TextSerializer(recent_text)
        return Response(serializer.data)


class GetContactByNumber(APIView):
    """Retrieve a contact by their phone number."""

    def get_object(self, number):
        """Get contact with given number."""
        return Contact.objects.get(number=number)

    def get(self, request, number=None, format=None):
        """Return json response."""
        contact = self.get_object('+' + str(number))
        serializer = ContactSerializer(contact)
        return Response(serializer.data)
