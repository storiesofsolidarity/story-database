from django.db import models
from django.db.models import Count
from django.db.models.signals import post_delete
from django.dispatch import receiver

from localflavor.us.models import USStateField

import geopy
from geopy.geocoders import GeoNames
from geopy.exc import GeopyError

from people.models import Author
from sos.cache import expire_view_cache


class LocationManager(models.Manager):
    def get_queryset(self):
        qs = super(LocationManager, self).get_queryset()
        qs_w_count = qs.annotate(story_grouped_count=Count('story'))
        return qs_w_count


class Location(models.Model):
    city = models.CharField(max_length=100, blank=True, null=True)
    state = USStateField(blank=True, null=True)
    county = models.CharField(max_length=100, null=True, blank=True)

    geocoded = models.BooleanField(default=False)

    lon = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)

    objects = LocationManager()

    #format city, state
    def city_formatter(self):
        if self.city:
            return ' '.join([p.capitalize() for p in self.city.split()])
        else:
            return ""
    city_formatter.short_description = "City"
    city_fmt = property(city_formatter)

    def state_formatter(self):
        if self.state:
            return self.state.upper()
        else:
            return ""
    state_formatter.short_description = "State"
    state_fmt = property(state_formatter)

    def __unicode__(self):
        return "{}, {}".format(self.city_fmt, self.state_fmt)

    def story_count(self):
        return self.story_grouped_count
    story_count.admin_order_field = 'story_grouped_count'

    def geocode(self, query):
        geolocator = GeoNames(username="jlevinger", country_bias="USA")
        location = geolocator.geocode(query)
        try:
            self.city = location.raw['toponymName']
            self.state = location.raw['adminCode1']
            self.lat = location.latitude
            self.lon = location.longitude
            self.geocoded = True
            self.save()
            return True
        except GeopyError:
            return False

    def reverse_geocode(self):
        geolocator = GeoNames(username="jlevinger", country_bias="USA")
        location = geolocator.reverse("%s, %s" % (self.lat, self.lon), exactly_one=True)
        try:
            self.city = location.raw['toponymName']
            self.state = location.raw['adminCode1']
            self.lat = location.latitude
            self.lon = location.longitude
            self.geocoded = True
            self.save()
            return True
        except GeopyError:
            return False


class Story(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    anonymous = models.BooleanField(default=False)

    author = models.ForeignKey(Author, null=True)
    location = models.ForeignKey(Location, null=True)

    content = models.TextField()
    display = models.BooleanField(default=True)
    truncated = models.BooleanField(default=False, help_text="Some legacy stories truncated")

    class Meta:
        verbose_name_plural = "stories"
        ordering = ("-created_at",)

    def excerpt(self):
        if len(self.content) > 160:
            return self.content[:160] + ' ...'
        else:
            return self.content

    def employer(self):
        if self.author:
            return self.author.employer
        else:
            return None

    def __unicode__(self):
        if self.anonymous:
            return "Story by Anonymous"
        else:
            return "Story, by {}".format(self.author)


@receiver(post_delete, sender=Story)
def clear_location_cache(sender, **kwargs):
    return expire_view_cache('location-list')
