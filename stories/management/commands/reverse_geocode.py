from django.core.management.base import BaseCommand
from django.db.models import Q

from stories.models import Location


class Command(BaseCommand):
    help = """Reverse geocode locations to City / State"""

    def handle(self, *args, **options):
        ungeocoded = Location.objects.filter(lat__isnull=False, lon__isnull=False) \
                                     .filter((Q(city__isnull=True) | Q(city='')))
        print ungeocoded.count(), "locations to reverse geocode"
        for location in ungeocoded:
            success = location.reverse_geocode()
            if not success:
                print "failed to geocode", location
                location.geocoded = False
                location.save()
        print "done"
