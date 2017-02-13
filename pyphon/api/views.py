from texts.models import Text
from api.serializers import TextSerializer
from rest_framework import viewsets, permissions, views
from rest_framework.views import APIView

# from api.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response

from rest_framework_extensions.etag.mixins import ETAGMixin
from rest_framework_extensions.etag.decorators import etag


class TextViewSet(ETAGMixin, viewsets.ModelViewSet):

    serializer_class = TextSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def get_queryset(self):
        """Get queryset for photographer."""
        return Text.objects.all()


# class TextViewSet(ETAGMixin, viewsets.ModelViewSet):

#     serializer_class = TextSerializer
#     # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

#     @etag()
#     def list(self, request, *args, **kwargs):
#         return super(TextViewSet, self).list(request, *args, **kwargs)

#     @etag()
#     def retrieve(self, request, *args, **kwargs):
#         return super(TextViewSet, self).retrieve(request, *args, **kwargs)

#     def get_queryset(self):
#         """Get queryset for photographer."""
#         return Text.objects.all()
