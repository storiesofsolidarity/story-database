from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.contrib import admin

from rest_framework import routers

from stories.views import StoryViewSet, LocationViewSet
from people.views import AuthorViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'story', StoryViewSet)
router.register(r'location', LocationViewSet, base_name="Location")
router.register(r'author', AuthorViewSet)

urlpatterns = patterns('',
    url(r'^/$', RedirectView.as_view(url='http://storiesofsolidarity.org', permanent=False), name='index'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/', include(router.urls)), # nice api browser

    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api/auth/registration/', include('rest_auth.registration.urls')),
    # url(r'^sms/', include('sms.urls')), # post via sms
    url(r'^api/activity/', include('actstream.urls'))
)
admin.site.site_header = 'Stories of Solidarity Admin'