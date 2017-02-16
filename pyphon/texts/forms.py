from django import forms
from texts.models import Text
from contacts.models import Contact
from contacts.forms import ContactForm


class TextForm(forms.ModelForm):
    """Form for new text messages."""

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = ''

    class Meta:
        model = Text
        fields = ['body']


class NewTextForm(ContactForm):
    """Create a new contact from an input number."""
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['number'].label = ''

    class Meta:
        model = Contact
        fields = ['number']
