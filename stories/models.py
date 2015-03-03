from django.db import models
from localflavor.us.models import USZipCodeField, USStateField

from people.models import Author

class Location(models.Model):
    city = models.CharField(max_length=100)
    state = USStateField(null=True)
    zipcode = USZipCodeField(null=True)

    geocoded = models.BooleanField(default=False)

    lon = models.FloatField(null=True)
    lat = models.FloatField(null=True)

    # if we decide we need geodjango querying
    # objects = django.contrib.gis.db.models.GeoManager()


class Story(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    anonymous = models.BooleanField(default=False)

    user = models.ForeignKey(Author, null=True)
    title = models.CharField(max_length=255)
    location = models.ForeignKey(Location, null=True)

    content = models.TextField()
    display = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "stories"