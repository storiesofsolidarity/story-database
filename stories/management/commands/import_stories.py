from django.core.management.base import BaseCommand, CommandError

from stories.models import Story
from people.models import Author
from django.contrib.auth.models import User

import os, csv

class Command(BaseCommand):
    args = '<filename>'
    help = """Import the specified CSV of stories
            Expects a header like [first_name, last_name, story, image]"""

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('No filename specified')
        if not os.path.exists(args[0]):
            raise CommandError('Filename does not exist')

        with open(args[0],'r') as csvfile:
            stories = csv.DictReader(csvfile)

            n = 0
            for story in stories:
                user, new_user = User.objects.get_or_create(first_name=story['first_name'],last_name=story['last_name'])
                if new_user:
                    user.username = ("{}_{}".format(user.first_name, user.last_name)).lower()
                user.save()

                author, new_author = Author.objects.get_or_create(user=user)
                #if story['image']:
                #    author.photo = story['image']
                author.save()

                story = Story(author=author, content=story['story'])
                story.save()
                n = n + 1

            self.stdout.write("imported",n,"new stories")
