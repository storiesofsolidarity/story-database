from django.core.management.base import BaseCommand
from optparse import make_option

from stories.models import Story, Location
from people.models import Author
from django.contrib.auth.models import User

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

        with open('stories/fixtures/legacy-stories.json','r') as jsonfile:
            stories = json.load(jsonfile)

            n = 0
            for data in stories['data']:
                story = Story(content = data.get('Content'),
                              created_at = data.get('Timestamp'))

                # usernames actually stored in legacy story "Title" field
                story.title = ""
                if data.get('Title'):
                    try:
                        first_name, last_name = data['Title'].split(' ')
                    except ValueError:
                        first_name = ""
                        last_name = data['Title']
                    user, new_user = User.objects.get_or_create(first_name=first_name,last_name=last_name)
                    if new_user:
                        if first_name:
                            user.username = ("{}_{}".format(user.first_name, user.last_name)).lower()
                        else:
                            user.username = last_name
                        user.save()

                    author, new_author = Author.objects.get_or_create(user=user)
                    if new_author:
                        author.part_time = bool(data.get('PartTime'))
                        author.employed = bool(data.get('Employed'))
                        author.company = data.get('Workplace')
                        author.title = data.get('JobTitle')
                        if user.last_name.lower() == "anonymous":
                                author.anonymous = True

                        author.save()

                    story.author = author                    

                if data.get('Latitude') and data.get('Longitude'):
                    location, new_location = Location.objects.get_or_create(city = data.get('City'), state = data.get('State'))
                    if new_location and data.get('Latitude') and data.get('Longitude'):
                        location.lat = data.get('Latitude')
                        location.lon = data.get('Longitude')
                        location.geocoded = True
                    location.save()
                    story.location = location
                story.save()
                n = n+1

            self.stdout.write("imported %d stories" % n)
