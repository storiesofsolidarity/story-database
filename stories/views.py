from rest_framework import viewsets, permissions
from sos.pagination import LargeResultsSetPagination

from django.db.models import Count, Avg

from models import Story, Location
from serializers import StorySerializer, LocationSerializer


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.filter(display=True)
    serializer_class = StorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LocationSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        locations = Location.objects.filter(lat__isnull=False, lon__isnull=False)
        locations_grouped = locations.values('state','city').annotate(
            story_count = Count('story'),
            lon = Avg('lon'),
            lat = Avg('lat')
        )

        return locations_grouped
