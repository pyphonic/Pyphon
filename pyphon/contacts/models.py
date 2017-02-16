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
        body = self.texts.first().body
        if len(body) > 24:
            return self.texts.first().body[:20] + '...'
        return body

    def most_recent_time(self):
        time = self.texts.first().time
        if datetime.today().day == time.day:
            return time.strftime('%I:%M %p')
        return time.strftime('%m-%d')