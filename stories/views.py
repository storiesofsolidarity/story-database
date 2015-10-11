from django.db.models import Count

from rest_framework import viewsets
from sos.permissions import AllowAnonymousPostOrReadOnly
from sos.pagination import MediumResultsSetPagination, LargeResultsSetPagination

from models import Story, Location
from serializers import (StorySerializer, LocationStoriesSerializer,
    StateStoriesSerializer, CountyStoriesSerializer)

from localflavor.us.us_states import US_STATES
STATE_ABBRS = {v.replace(' ', '_'): k for k, v in US_STATES}  # convert state names to map format


class StoryViewSet(viewsets.ModelViewSet):
    serializer_class = StorySerializer
    permission_classes = (AllowAnonymousPostOrReadOnly, )
    # allow stories to be added by non-logged in users

    def get_queryset(self):
        # custom filtering by city/state instead of requiring location id
        params = self.request.QUERY_PARAMS
        queryset = Story.objects.filter(display=True).order_by('-created_at')
        state = params.get('state', None)
        if state:
            queryset = queryset.filter(location__state__iexact=state)
            city = params.get('city', None)
            if city:
                queryset = queryset.filter(location__city__iexact=city)
        return queryset


class StateStoriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (Story.objects.filter(location__isnull=False)
        .values('location__state')
        .annotate(Count('id', distinct=True))
        .order_by())
    serializer_class = StateStoriesSerializer


class CountyStoriesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CountyStoriesSerializer
    pagination_class = MediumResultsSetPagination

    def get_queryset(self):
        # custom filtering by city/state instead of requiring location id
        params = self.request.QUERY_PARAMS
        queryset = Story.objects.filter(location__isnull=False)
        state_name = params.get('state_name', None)
        if state_name:
            state = STATE_ABBRS.get(state_name)  # location.state field stores 2-char abbreviation
            queryset = queryset.filter(location__state__iexact=state)
        return (queryset.values('location__county')
            .annotate(Count('id', distinct=True))
            .order_by())


class LocationStoriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.filter(lat__isnull=False, lon__isnull=False, story_grouped_count__gt=0)
    serializer_class = LocationStoriesSerializer
    pagination_class = LargeResultsSetPagination
