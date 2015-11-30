from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.contrib import admin

from rest_framework import routers

from stories.views import (StoryViewSet, SearchStoriesViewSet,
    StateStoriesViewSet, CountyStoriesViewSet, LocationStoriesViewSet)
from people.views import AuthorViewSet

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'story', StoryViewSet, base_name="story")
router.register(r'state', StateStoriesViewSet, base_name="state")
router.register(r'county', CountyStoriesViewSet, base_name="county")
router.register(r'location', LocationStoriesViewSet, base_name="location")
router.register(r'author', AuthorViewSet, base_name="author")
router.register(r'search', SearchStoriesViewSet, base_name="search")

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='https://storiesofsolidarity.org'), name='index'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include(router.urls)),  # nice api browser

    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api/auth/registration/', include('rest_auth.registration.urls')),
    url(r'^sms/', include('sms.urls')),  # post via sms
    url(r'^api/activity/', include('actstream.urls'))
)
if settings.DEBUG:
    urlpatterns.append(url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
    	{'document_root': settings.MEDIA_ROOT}))
admin.site.site_header = 'Stories of Solidarity Admin'
