from django.db import models
# from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Contact(models.Model):
    """Text messages."""
    name = models.CharField(max_length=255, default="")
    number = PhoneNumberField(unique=True)

    def __str__(self):
        """Return title as string."""
        if self.name:
            return self.name
        return str(self.number)

    def format_number(self):
        """Return formatted phone number."""
        num = str(self.number)
        return "({}) {}-{}".format(num[2:5], num[5:8], num[8:])
