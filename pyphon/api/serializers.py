from rest_framework import serializers
from texts.models import Text


class TextSerializer(serializers.ModelSerializer):
    # sender = serializers.ReadOnlyField(source='owner.username')
    # The above came from imager. maybe needs to be different.

    class Meta:
        model = Text
        fields = (
            'body',
            'time',
            'sender'
        )
