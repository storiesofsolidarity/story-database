from twilio import twiml
from django_twilio.decorators import twilio_view
from django_twilio.request import decompose
import re

from django.contrib.auth.models import User
from people.models import Author
from stories.models import Story, Location


@twilio_view
def sms_post(request):
    try:
        response = twiml.Response()
        twilio_request = decompose(request)

        if twilio_request.type is 'message':
            print twilio_request.body, twilio_request.from_, twilio_request.fromcity, twilio_request.fromstate
            try:
                author = Author.objects.get(sms_number=twilio_request.from_)
            except Author.DoesNotExist:
                first_name = "Anonymous"
                last_anon = User.objects.filter(first_name=first_name).count()
                last_name = "SMS#%d" % (last_anon+1,)
                username = "{}_{}".format(first_name, last_name).lower()
                user, new_user = User.objects.get_or_create(first_name=first_name, last_name=last_name, username=username)
                author = Author(user=user, sms_number=twilio_request.from_)
                author.save()

            zipcode_match = re.search('(\d{5})([- ])?(\d{4})?', twilio_request.body)
            if zipcode_match:
                zipcode = zipcode_match.group(0)
                location = Location()
                location.geocode(zipcode)
            else:
                #try to guess it from phone number location
                location, new_location = Location.objects.get_or_create(city=twilio_request.fromcity, state=twilio_request.fromstate)
            story = Story(author=author, content=twilio_request.body, location=location)
            print story
            story.save()

            response.message('Thanks for sharing your Story of Solidarity')
            # TODO, respond with request for zipcode
            # TODO, try to sign user up with email
            return response
        else:
            print "unhandled request type", twilio_request

    except Exception:
        import traceback
        print traceback.format_exc()

    return response
