from rest_framework import viewsets, permissions

from models import Story, Location
from serializers import StorySerializer, LocationSerializer

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly)

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly)
