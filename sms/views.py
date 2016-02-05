from twilio import twiml
from django_twilio.decorators import twilio_view
from django_twilio.request import decompose
import re
import requests

from django.contrib.auth.models import User
from people.models import Author
from stories.models import Story, Location


def new_story(request, twilio_request, response=twiml.Response()):
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

    story = Story(author=author, content=twilio_request.body)
    story.save()

    # save storyId for continuation
    request.set_cookie('storyId', story.id)

    response.message("Thank you for sharing with StoriesOfSolidarity.org" +
                     " Now put your story on the map! Reply with your zipcode for accurate posting.")
    return response
    # TODO, try to sign user up with email


def clear_cookie(request, twilio_request, response=twiml.Response()):
    request.delete_cookie('storyId')
    response.message('Cleared storyId cookie. Further texts from this number will be treated as new submissions.')
    return response


def match_zipcode(request, twilio_request, response=twiml.Response()):
    zipcode_match = re.search('(\d{5})([- ])?(\d{4})?', twilio_request.body)
    if zipcode_match:
        zipcode = zipcode_match.group(0)
        r = requests.get('https://api.zippopotam.us/us/%s' % zipcode)
        # use zippopotamus for quick zipcode -> city/state lookup
        # mapzen is surprisingly bad at this
        try:
            match = r.json()['places'][0]
            if match:
                location, created = Location.objects.get_or_create(zipcode=zipcode)
                if created:
                    query_string = '%(place name)s %(state abbreviation)s' % match
                    location.geocode(query_string)
                    location.save()
                return location
        except (ValueError, IndexError):
            pass
    return False


@twilio_view
def sms_post(request):
    # try to fake out the request.is_ajax method, so we send twilio better error messages
    request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

    try:
        response = twiml.Response()
        twilio_request = decompose(request)

        if twilio_request.type is 'message':
            # check commands first
            commands = {'CLEAR': clear_cookie}
            for (cmd, fn) in commands.items():
                if twilio_request.body.startswith(cmd):
                    return fn(request, twilio_request, response)

            # then continuation of existing, set by cookie
            storyId = None
            if 'storyId' in request.COOKIES:
                try:
                    storyId = int(request.COOKIES.get('storyId'))
                except ValueError:
                    pass

            if storyId:
                story = Story.objects.get(id=request.COOKIES.get('storyId'))

                # check if zipcode location update
                zipcode_location = match_zipcode(request, twilio_request)
                if zipcode_location:
                    story.location = zipcode_location
                    story.save()
                    response.message('Thank you for adding a location to your story. Find it on the map at StoriesOfSolidarity.org')
                    return response
                else:
                    # it's a continuation of the previous content
                    story.content = story.content + " " + twilio_request.body
                    story.save()
                    return response

            # then new story
            return new_story(request, twilio_request, response)
        else:
            return response
    except Exception:
        import traceback
        print traceback.format_exc()
