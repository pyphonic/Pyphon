from django import forms
from texts.models import Text


class TextForm(forms.ModelForm):
    """Form for new text messages."""

    class Meta:
        model = Text
        fields = ['body']
