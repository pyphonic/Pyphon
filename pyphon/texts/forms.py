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
        widgets = {
            'body': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }


class NewTextForm(ContactForm):
    """Create a new contact from an input number."""

    class Meta:
        model = Contact
        exclude = ['name']
        widgets = {
            'body': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }
