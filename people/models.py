from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User)
    company = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=100, null=True)

    photo = models.ImageField(null=True, upload_to="author_photo")

    employed = models.BooleanField(default=True)
    part_time = models.BooleanField(default=False)

class Organizer(models.Model):
    user = models.OneToOneField(User)
    organization = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    # city, state, zip
    # website
