from django.core.management.base import BaseCommand
from optparse import make_option
from datetime import datetime

from stories.models import Story, Location
from people.models import Author

import json


class Command(BaseCommand):
    args = '<filename> --flush'
    help = """Import a JSON of stories from the prototype site"""
    option_list = BaseCommand.option_list + (
        make_option('--flush',
                    action='store_true',
                    dest='flush',
                    default=False,
                    help='Delete all stories before importing legacy'),
        )

    def handle(self, *args, **options):
        if options['flush']:
            old = Story.objects.all()
            confirm = raw_input('This will delete all %d existing stories. Are you sure? [y/N] ' % old.count())
            if confirm == 'y':
                old.delete()

        with open('stories/fixtures/legacy-stories.json', 'r') as jsonfile:
            stories = json.load(jsonfile)

            n_s, n_a = (0, 0)
            for data in stories['data']:
                story = Story(content=data.get('Content'))

                author, new_author = Author.objects.get_or_create_user(user__name=data.get('UserName'))
                if new_author:
                    n_a = n_a+1
                    author.part_time = bool(data.get('PartTime'))
                    author.employed = bool(data.get('Employed'))
                    author.employer = data.get('Employer')
                    author.occupation = data.get('Occupation')
                    if author.user.last_name.lower() == "anonymous":
                        author.anonymous = True

                    author.save()
                story.author = author

                if data.get('Truncated'):
                    story.truncated = True

                if data.get('Latitude') and data.get('Longitude'):
                    location, new_location = Location.objects.get_or_create(city=data.get('City'), state=data.get('State'))
                    if new_location and data.get('Latitude') and data.get('Longitude'):
                        location.lat = data.get('Latitude')
                        location.lon = data.get('Longitude')
                        location.geocoded = True
                    location.save()
                    story.location = location
                story.save()
                if data.get('Timestamp'):
                    story.created_at = data['Timestamp']
                else:
                    # old, put it before anything else
                    story.created_at = datetime(2013, 7, 1, 0, 0)
                story.updated_at = datetime.now()
                story.save()

                n_s = n_s+1

            self.stdout.write("imported %d stories by %d authors" % (n_s, n_a))
