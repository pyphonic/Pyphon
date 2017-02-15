from django.db import models
from django.utils import timezone
from contacts.models import Contact


class Call(models.Model):
    """Database model for phone calls."""

    contact = models.ForeignKey(Contact, related_name='calls', null=True)
    time = models.DateTimeField(default=timezone.now)
    directions = [
        ('incoming', 'incoming'),
        ('outgoing', 'outgoing'),
    ]
    direction = models.CharField(choices=directions, max_length=10)
    statuses = [
        ('no-answer', 'no-answer'),
        ('completed', 'completed'),
        ('canceled', 'canceled'),
        ('busy', 'busy'),
        ('failed', 'failed'),
        ('other', 'other')
    ]
    status = models.CharField(choices=statuses, max_length=10, blank=True, null=True)
