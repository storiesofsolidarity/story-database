from django.core.management.base import BaseCommand
from django.db.models import Q

from stories.models import Location


class Command(BaseCommand):
    help = """Reverse geocode locations from lat/lon to city/county/state"""

    def handle(self, *args, **options):
        ungeocoded = Location.objects.filter(lat__isnull=False, lon__isnull=False) \
                                     .filter((Q(county__isnull=True) | Q(county='')))
        print ungeocoded.count(), "locations to reverse geocode"
        for (index, location) in enumerate(ungeocoded):
            try:
                success = location.reverse_geocode()
            except Exception,e:
                print index," failure", e
                location.geocoded = False
                location.save()
            if success:
                print index, "geocoded", location
            else:
                print index, "failed to geocode", location
                location.geocoded = False
                location.save()

        print "done"
