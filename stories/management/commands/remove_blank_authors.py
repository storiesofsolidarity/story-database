from django.core.management.base import BaseCommand
from django.db.models import Count

from people.models import Author


class Command(BaseCommand):
    help = """Remove authors without stories"""

    def handle(self, *args, **options):
        blank_authors = Author.objects.annotate(story_count=Count('story')).filter(story_count=0)
        print blank_authors.count(), "authors without stories"
        for a in blank_authors:
            a.user.delete()
            a.delete()
        print "done"
