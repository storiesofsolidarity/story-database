from django.conf.urls import patterns, url
from sms.views import sms_post

urlpatterns = patterns('sms',
    url(r'^post', sms_post)
)
