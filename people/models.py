from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    employer = models.CharField(max_length=100, null=True, blank=True)

    photo = models.ImageField(blank=True, null=True, upload_to="author_photo")
    sms_number = models.CharField(blank=True, null=True, max_length=15)

    employed = models.BooleanField(default=True)
    part_time = models.BooleanField(default=False)

    anonymous = models.BooleanField(default=False, help_text=
            "Group account like 'Web Anonymous' or 'SMS Anonymous'")

    def __unicode__(self):
        if self.title and self.company:
            return "{}, {}, {}".format(self.user, self.title, self.company)
        elif self.user:
            return self.user.__unicode__()
        else:
            return "Unnamed Author"


class Organizer(models.Model):
    user = models.OneToOneField(User)
    organization = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    # city, state, zip
    # website
