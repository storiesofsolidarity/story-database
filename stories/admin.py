from django.contrib import admin
from models import Location, Story


class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'state', 'story_count')
    list_filter = ('state',)

admin.site.register(Location, LocationAdmin)


class StoryAdmin(admin.ModelAdmin):
    list_display = ('excerpt', 'author', 'created_at')
    date_filter = ('created_at',)

admin.site.register(Story, StoryAdmin)
