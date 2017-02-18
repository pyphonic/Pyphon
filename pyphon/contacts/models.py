from django.db import models
# from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime
# Create your models here.


class Contact(models.Model):
    """Text messages."""
    name = models.CharField(max_length=255, default="")
    number = PhoneNumberField(unique=True)

    def __str__(self):
        """Return title as string."""
        if self.name:
            return self.name
        num = str(self.number)
        return "({}) {}-{}".format(num[2:5], num[5:8], num[8:])

    def format_number(self):
        """Return formatted phone number."""
        num = str(self.number)
        return "({}) {}-{}".format(num[2:5], num[5:8], num[8:])

    def most_recent_text(self):
        """Return a contact's most recent text."""
        return self.texts.order_by('id').reverse()[0]

    def most_recent_text_body(self):
        """Return body of most recent text."""
        body = self.most_recent_text().body
        if len(body) > 24:
            return self.texts.first().body[:20] + '...'
        return body

    def most_recent_time(self):
        """Return time of most recent text."""
        time = self.most_recent_text().time
        if datetime.today().day == time.day:
            return time.strftime('%I:%M %p')
        return time.strftime('%b %d')

    def most_recent_text_id(self):
        """Return id of most recent text."""
        return self.most_recent_text().id
