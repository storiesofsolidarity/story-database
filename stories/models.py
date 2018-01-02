import requests

from django.conf import settings
from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from localflavor.us.models import USStateField
from localflavor.us.us_states import STATE_CHOICES

from people.models import Author
from sos.cache import expire_view_cache

STATE_NAMES = [(item[1]) for item in STATE_CHOICES]
STATE_ABBRS = dict((item[1],item[0]) for item in STATE_CHOICES)

class LocationManager(models.Manager):
    def get_queryset(self):
        qs = super(LocationManager, self).get_queryset()
        qs_w_count = qs.annotate(story_grouped_count=Count('story'))
        return qs_w_count


class Location(models.Model):
    state = USStateField(blank=True, null=True)
    county = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=5, null=True, blank=True)

    geocoded = models.BooleanField(default=False)
    lon = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)

    objects = LocationManager()

    #format city, county, state
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

    def county_formatter(self):
        if self.county:
            return self.county.replace(' County', '')
        else:
            return ""
    county_formatter.short_description = "County"
    county_fmt = property(county_formatter)

    def __unicode__(self):
        return "{}, {}".format(self.city_fmt, self.state_fmt)

    def story_count(self):
        return self.story_grouped_count
    story_count.admin_order_field = 'story_grouped_count'

    def geocode(self, query):
        payload = {
            'countrycodes': 'US',  # bias search response
            'q': query,
            'format': 'jsonv2'
        }
        headers = {'user-agent': 'stories-of-solidarity'}
        r = requests.get('https://nominatim.openstreetmap.org/search', params=payload, headers=headers)
        try:
            match = r.json()[0] # returns multiple matches, pick first
            if match:
                self.lat = match['lat']
                self.lon = match['lon']
                # run coordinates through reverse to get fullly parsed fields
                self.reverse_geocode()
                return True
            else:
                return False
        except (ValueError, IndexError):
            return False

    def reverse_geocode(self):
        payload = {
            'lat': self.lat,
            'lon': self.lon,
            'format': 'jsonv2'
        }
        headers = {'user-agent': 'stories-of-solidarity'}
        r = requests.get('https://nominatim.openstreetmap.org/reverse', params=payload, headers=headers)
        try:
            match = r.json() # only returns one match
            self.zipcode = match['address'].get('postcode')[:5]
            # OSM has weird locality hierarchy, gotta check em all
            for locality in ['city', 'town', 'village', 'hamlet']:
                if locality in match['address']:
                    self.city = match['address'][locality]
            self.county = match['address'].get('county')
            state_name = match['address'].get('state') #
            # store 2-character abbr to model
            self.state = STATE_ABBRS.get(state_name)
            self.geocoded = True
            self.save()
            return True
        except (ValueError, IndexError):
            return False


class Story(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    anonymous = models.BooleanField(default=False)

    author = models.ForeignKey(Author, null=True)
    location = models.ForeignKey(Location, null=True)

    content = models.TextField()
    photo = models.ImageField(upload_to='photos', blank=True, null=True)
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

    def author_display(self):
        if self.anonymous:
            return "Anonymous"
        else:
            return self.author.user_display()
    author_display.short_description = "Author"

    def __unicode__(self):
        if self.anonymous:
            return "Story by Anonymous"
        else:
            return "Story, by {}".format(self.author.user_display())


@receiver(post_save, sender=Story)
@receiver(post_delete, sender=Story)
def clear_story_cache(sender, **kwargs):
    expire_view_cache('story-list')
    expire_view_cache('state-list')
    expire_view_cache('county-list')
    expire_view_cache('location-list')


@receiver(post_save, sender=Location)
def clear_location_cache(sender, **kwargs):
    expire_view_cache('location-list')
