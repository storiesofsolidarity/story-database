from rest_framework import viewsets, permissions
from sos.pagination import LargeResultsSetPagination

from models import Story, Location
from serializers import StorySerializer, LocationStoriesSerializer


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.filter(display=True)
    serializer_class = StorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class LocationStoriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.filter(lat__isnull=False, lon__isnull=False, story_grouped_count__gt=0)
    serializer_class = LocationStoriesSerializer
    pagination_class = LargeResultsSetPagination
