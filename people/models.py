from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User)
    company = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=100, null=True)

    photo = models.ImageField(null=True, upload_to="author_photo")

    employed = models.BooleanField(default=True)
    part_time = models.BooleanField(default=False)

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
