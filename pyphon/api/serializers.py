from rest_framework import serializers
from texts.models import Text
from calls.models import Call
from contacts.models import Contact


class TextSerializer(serializers.ModelSerializer):
    # sender = serializers.ReadOnlyField(source='owner.username')
    # The above came from imager. maybe needs to be different.

    class Meta:
        model = Text
        fields = (
            'body',
            'time',
            'sender',
            'contact'
        )


class CallSerializer(serializers.ModelSerializer):
    """Callllls."""

    class Meta:
        model = Call
        fields = (
            'direction',
            'time',
            'status',
            'contact'
        )


class ContactSerializer(serializers.ModelSerializer):
    """Callllls."""

    class Meta:
        model = Contact
        fields = (
            'number',
            'name',
        )
