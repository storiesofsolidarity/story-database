from django.db.models import Count

from rest_framework import viewsets
from sos.permissions import AllowAnonymousPostOrReadOnly
from sos.pagination import MediumResultsSetPagination, LargeResultsSetPagination

from models import Story, Location
from serializers import (StorySerializer, LocationStoriesSerializer,
    StateStoriesSerializer, CountyStoriesSerializer, ZipcodeStoriesSerializer)

from localflavor.us.us_states import US_STATES
STATE_ABBRS = {v: k for k, v in US_STATES}  # convert state names to map format


class StoryViewSet(viewsets.ModelViewSet):
    serializer_class = StorySerializer
    permission_classes = (AllowAnonymousPostOrReadOnly, )
    # allow stories to be added by non-logged in users

    def get_queryset(self):
        # custom filtering by location state/county/city/zipcode instead of requiring id
        params = self.request.QUERY_PARAMS
        queryset = Story.objects.filter(display=True).order_by('-created_at')
        state = params.get('state', None)
        state_name = params.get('state_name', None)
        if state_name:
            state = STATE_ABBRS.get(state_name)  # location.state field stores 2-char abbreviation

        if state:
            queryset = queryset.filter(location__state__iexact=state)
            county = params.get('county', None)
            if county:
                queryset = queryset.filter(location__county__startswith=county)
            city = params.get('city', None)
            if city:
                queryset = queryset.filter(location__city__iexact=city)

        zipcode = params.get('zipcode', None)
        if zipcode:
            queryset = queryset.filter(location__zipcode=zipcode)

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


class ZipcodeStoriesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ZipcodeStoriesSerializer
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        # custom filtering by city/state instead of requiring location id
        params = self.request.QUERY_PARAMS
        queryset = Story.objects.filter(location__isnull=False)
        state_name = params.get('state_name', None)
        if state_name:
            state = STATE_ABBRS.get(state_name)  # location.state field stores 2-char abbreviation
            queryset = queryset.filter(location__state__iexact=state)

        return (queryset.values('location__zipcode')
            .annotate(Count('id', distinct=True))
            .order_by())


class SearchStoriesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StorySerializer

    def get_queryset(self):
        # custom filtering by content
        params = self.request.QUERY_PARAMS
        queryset = Story.objects.filter(display=True).order_by('-created_at')
        content = params.get('content', None)
        if content:
            queryset = queryset.filter(content__icontains=content)

        return queryset


# TO REMOVE
class LocationStoriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.filter(lat__isnull=False, lon__isnull=False, story_grouped_count__gt=0)
    serializer_class = LocationStoriesSerializer
    pagination_class = LargeResultsSetPagination
