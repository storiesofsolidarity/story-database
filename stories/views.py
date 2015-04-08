from rest_framework import viewsets, permissions
from sos.pagination import LargeResultsSetPagination

from models import Story, Location
from serializers import StorySerializer, LocationSerializer


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.filter(display=True)
    serializer_class = StorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.filter(lat__isnull=False, lon__isnull=False, story_grouped_count__gt=0)
    serializer_class = LocationSerializer
    pagination_class = LargeResultsSetPagination
