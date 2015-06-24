from django.core.management.base import BaseCommand
from optparse import make_option
from datetime import datetime

from stories.models import Story, Location
from people.models import Author

import fileinput, tempfile
import json
import requests
from unidecode import unidecode

class Command(BaseCommand):
    args = '<filename> --flush'
    help = """Import a JSON of stories from the OurWalmart"""
    option_list = BaseCommand.option_list + (
        make_option('--flush',
                    action='store_true',
                    dest='flush',
                    default=False,
                    help='Delete all stories before importing walmart stories'),
        )

    def handle(self, *args, **options):
        if options['flush']:
            old = Story.objects.filter(employer__startswith="Walmart")
            confirm = raw_input('This will delete all %d existing Walmart stories. Are you sure? [y/N] ' % old.count())
            if confirm == 'y':
                old.delete()

        # get input_file from stdin
        input_file = fileinput.input(args)
        temp_file = tempfile.TemporaryFile()
        # save to temp storage for json parsing
        for line in input_file:
            temp_file.write(line)
        temp_file.seek(0)

        with temp_file as jsonfile:
            stories = json.load(jsonfile)

            n_s, n_a, n_l = (0, 0, 0)
            for data in stories:
                try:
                    story, new_story = Story.objects.get_or_create(content=data.get('story'))
                except Story.MultipleObjectsReturned:
                    duplicates = Story.objects.filter(content=data.get('story'))
                    duplicates.delete()

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
                    city = place.get('place name')
                    state = place.get('state abbreviation')
                    lat, lon = place.get('latitude'), place.get('longitude')

                    try:
                        location, new_location = Location.objects.get_or_create(city__iexact=city, state=state)
                    except Location.MultipleObjectsReturned:
                        duplicate_locations = Location.objects.filter(city__iexact=city, state=state)
                        stories_at_location = duplicate_locations.values_list('story', flat=True)
                        duplicate_locations.delete()

                        location = Location(city=city, state=state)
                        location.save()

                        for reset_id in stories_at_location:
                            try:
                                reset_story = Story.objects.get(id=reset_id)
                                reset_story.location = location
                                reset_story.save()
                            except Story.DoesNotExist:
                                pass

                        new_location = True
                        
                    if new_location and lat and lon:
                        location.city = city
                        location.state = state
                        location.lat = lat
                        location.lon = lon
                        location.geocoded = True
                        location.save()

                        n_l = n_l+1

                    story.location = location
                story.save()

                # export date from OurWalmart
                story.created_at = datetime(2013, 9, 4, 0, 0)
                story.updated_at = datetime.now()

                story.save()

                if new_story:
                    n_s = n_s+1

            self.stdout.write("imported %d stories by %d authors in %d locations" % (n_s, n_a, n_l))
