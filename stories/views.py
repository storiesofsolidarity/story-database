from rest_framework import viewsets, permissions

from models import Story, Location
from serializers import StorySerializer, LocationSerializer

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.filter(display=True)
    serializer_class = StorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly)

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.filter(lat__is_null=False, lon__is_null=False)
    serializer_class = LocationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly)
