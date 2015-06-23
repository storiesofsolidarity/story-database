from django.core.management.base import BaseCommand
from optparse import make_option
from datetime import datetime

from stories.models import Story, Location
from people.models import Author

import codecs
import json
import requests
from unidecode import unidecode

class Command(BaseCommand):
    args = '<filename> --flush'
    help = """Import a JSON of stories from the prototype site"""
    option_list = BaseCommand.option_list + (
        make_option('--flush',
                    action='store_true',
                    dest='flush',
                    default=False,
                    help='Delete all stories before importing walmart'),
        )

    def handle(self, *args, **options):
        if options['flush']:
            old = Story.objects.all()
            confirm = raw_input('This will delete all %d existing stories. Are you sure? [y/N] ' % old.count())
            if confirm == 'y':
                old.delete()

        with codecs.open('stories/fixtures/walmart-faces.json', 'r', encoding='utf-8') as jsonfile:
            stories = json.load(jsonfile)

            n_s, n_a = (0, 0)
            for data in stories:
                story = Story(content=data.get('story'))

                first_name = unidecode(data.get('fname'))
                last_name = unidecode(data.get('lname'))

                author, new_author = Author.objects.get_or_create_user(first_name=first_name, last_name=last_name)
                if new_author:
                    n_a = n_a+1

                    if data.get('email'):
                        author.user.email = data.get('email')

                    author.user.active = False
                    author.user.save()

                    if data.get('store'):
                        author.employer = "Walmart #"+data.get('store')
                    else:
                        author.employer = "Walmart"

                    if data.get('associate'):
                        author.occupation = "Associate"

                    if data.get('anonymous'):
                        author.anonymous = True

                    author.save()

                story.author = author

                if data.get('zip'):
                    zipcode = data.get('zip')

                    # do zip -> city lookup inline
                    zip_lookup = requests.get("http://api.zippopotam.us/us/"+zipcode)
                    print "lookup", zipcode
                    place = zip_lookup.json().get('places', [{}])[0]

                    location, new_location = Location.objects.get_or_create(city=place.get('place name'), state=place.get('state abbreviation'))
                    if new_location and place.get('latitude') and place.get('longitude'):
                        location.lat = place.get('latitude')
                        location.lon = place.get('longitude')
                        location.geocoded = True
                        location.save()
                    story.location = location
                story.save()

                # export date from OurWalmart
                story.created_at = datetime(2013, 9, 4, 0, 0)
                story.updated_at = datetime.now()

                story.save()

                n_s = n_s+1

            self.stdout.write("imported %d stories by %d authors" % (n_s, n_a))
