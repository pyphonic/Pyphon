from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView

from contacts.models import Contact


# # Create your views here.
# class ContactIdView(TemplateView):
#     """Class based view for individual photo view."""

#     template_name = "imager_images/photo_id.html"

#     def get_context_data(self, pk):
#         """Extending get_context_data method for our data."""
#         contact = Contact.objects.get(pk=pk)
#         if photo.published == 'public' or photo.owner.user == self.request.user:
#             return {"photo": photo}
#         else:
#             error = "I'm sorry, that photo is not available."
#             return {"error": error}
