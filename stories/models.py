from django.db import models
from localflavor.us.models import USStateField

from django.db.models import Count

from people.models import Author

class LocationManager(models.Manager):
    def get_queryset(self):
        qs = super(LocationManager,self).get_queryset()
        qs_w_count = qs.annotate( story_grouped_count = Count('story') )
        return qs_w_count

class Location(models.Model):
    city = models.CharField(max_length=100)
    state = USStateField(null=True)
    county = models.CharField(max_length=100, null=True, blank=True)

    geocoded = models.BooleanField(default=False)

    lon = models.FloatField(null=True)
    lat = models.FloatField(null=True)

    objects = LocationManager()

    def __unicode__(self):
        return "{}, {}".format(self.city,self.state)

    def story_count(self):
        return self.story_grouped_count
    story_count.admin_order_field = 'story_grouped_count'


class Story(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    anonymous = models.BooleanField(default=False)

    author = models.ForeignKey(Author, null=True)
    title = models.CharField(max_length=255)
    location = models.ForeignKey(Location, null=True)

    content = models.TextField()
    display = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "stories"

    def __unicode__(self):
        if self.anonymous:
            if self.title:
                return "{}, by Anonymous".format(self.title)
            else:
                return "Untitled Story, by Anonymous"      
        else:
            if self.title:
                if self.author:
                    return "{}, by {}".format(self.title,self.author)
                else:
                    return self.title
            else:
                return "Untitled Story, by {}".format(self.author)