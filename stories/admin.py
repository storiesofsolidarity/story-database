from django.contrib import admin
from models import Location, Story

class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'state', 'story_count')
    list_filter = ('state',)

admin.site.register(Location, LocationAdmin)
admin.site.register(Story)
