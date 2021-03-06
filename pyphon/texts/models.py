from django.db import models
from django.utils import timezone
from contacts.models import Contact


# Create your models here.

class Text(models.Model):
    """Text messages."""
    body = models.CharField(max_length=300)
    time = models.DateTimeField(default=timezone.now)
    senders = [('you', 'You'),
               ('them', 'Them')]
    sender = models.CharField(choices=senders, max_length=12)
    contact = models.ForeignKey(Contact, related_name='texts', null=True)

    def __str__(self):
        """Return title as string."""
        return self.body[:20]
