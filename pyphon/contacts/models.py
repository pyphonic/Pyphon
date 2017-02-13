from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Contact(models.Model):
    """Text messages."""
    name = models.CharField(max_length=255, default="")
    number = PhoneNumberField()

    def __repr__(self):
        """Return title as string."""
        if self.name:
            return self.name
        return str(self.number)
