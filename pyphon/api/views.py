from texts.models import Text
from api.serializers import TextSerializer
from rest_framework import viewsets, permissions
from api.permissions import IsOwnerOrReadOnly


class TextViewSet(viewsets.ModelViewSet):

    serializer_class = TextSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def get_queryset(self):
        """Get queryset for photographer."""
        return Text.objects.all()
