from django.shortcuts import render
from django.views.generic import ListView, CreateView
from texts.models import Text
from texts.forms import TextForm
from django.views.generic.edit import ModelFormMixin


class TextView(ListView, ModelFormMixin):
    """A view for the texts."""
    model = Text
    form_class = TextForm

    template_name = "texts/texting.html"
    context_object_name = "texts"

    def get_queryset(self):
        last_ten = Text.objects.all().order_by('-id')[:10][::-1]
        return last_ten

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        # Explicitly states what get to call:
        return ListView.get(self, request, *args, **kwargs)

    def form_valid(self, form):
        """Execute if form is valid."""
        self.object = self.get_object()
        text = form.save()
        text.sender = 'you'
        text.save()

    def post(self, request, *args, **kwargs):
        # When the form is submitted, it will enter here
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            # self.object = self.form.save()
            # Here ou may consider creating a new instance of form_class(),
            # so that the form will come clean.
            text = self.form.save()
            text.sender = 'you'
            text.save()
        # Whether the form validates or not, the view will be rendered by get()
        return self.get(request, *args, **kwargs)
