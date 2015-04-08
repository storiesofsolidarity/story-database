from rest_framework import viewsets, permissions
from sos.pagination import LargeResultsSetPagination

from models import Story, Location
from serializers import StorySerializer, LocationStoriesSerializer


class StoryViewSet(viewsets.ModelViewSet):
    serializer_class = StorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        params = self.request.QUERY_PARAMS
        queryset = Story.objects.filter(display=True)
        state = params.get('state', None)
        if state:
            queryset = queryset.filter(location__state__iexact=state)
            city = params.get('city', None)
            if city:
                queryset = queryset.filter(location__city__iexact=city)
        return queryset

class LocationStoriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.filter(lat__isnull=False, lon__isnull=False, story_grouped_count__gt=0)
    serializer_class = LocationStoriesSerializer
    pagination_class = LargeResultsSetPagination
