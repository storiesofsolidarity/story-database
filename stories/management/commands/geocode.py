from django.core.management.base import BaseCommand
from stories.models import Location


class Command(BaseCommand):
    help = """Geocode story locations"""

    def handle(self, *args, **options):
        ungeocoded = Location.objects.filter(lat=None, lon=None, geocoded=False, city__isnull=False, state__isnull=False)
        print ungeocoded.count(), "locations to geocode"
        for location in ungeocoded:
            success = location.geocode("%s, %s" % (location.city, location.state))
            if not success:
                print "failed to geocode", location
                location.geocoded = False
                location.save()
        print "done"
