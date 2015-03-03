from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.contrib import admin

from rest_framework import routers

from stories.views import StoryViewSet, LocationViewSet
from people.views import AuthorViewSet

router = routers.DefaultRouter()
router.register(r'stories', StoryViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'authors', AuthorViewSet)

urlpatterns = patterns('',
    url(r'^/$', RedirectView.as_view(url='http://storiesofsolidarity.org', permanent=False), name='index'),
    url(r'^admin/', include(admin.site.urls)),
    # login, logout

    url(r'^activity/', include('actstream.urls')),
    # post via sms

    url(r'^api/', include(router.urls)), # nice api browser
)
admin.site.site_header = 'Stories of Solidarity Admin'