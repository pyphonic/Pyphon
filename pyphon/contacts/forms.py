from django import forms
from contacts.models import Contact


class ContactForm(forms.ModelForm):
    """Form for new contacts."""

    class Meta:
        model = Text
        fields = ['name', 'number']
