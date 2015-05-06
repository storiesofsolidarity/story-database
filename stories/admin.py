from django.contrib import admin
from models import Location, Story
from people.models import Author


class LocationAdmin(admin.ModelAdmin):
    list_display = ('city_fmt', 'state_fmt', 'story_count')
    list_filter = ('state',)
    search_fields = ('city',)

admin.site.register(Location, LocationAdmin)


class EmployerFilter(admin.SimpleListFilter):
    title = 'author employer'
    parameter_name = 'employer'

    def lookups(self, request, model_admin):
        employers = set([a.employer for a in Author.objects.all()])
        return [(str(c), str(c)) for c in employers if c]

    def queryset(self, request, queryset):
        if self.value() or self.value() == 'None':
            return queryset.filter(author__employer=self.value())
        else:
            return queryset


class StoryAdmin(admin.ModelAdmin):
    list_display = ('excerpt', 'author', 'employer', 'created_at')
    list_filter = (EmployerFilter, 'location__state', 'truncated')
    date_hierarchy = 'created_at'
    readonly_fields = ('truncated',)
    raw_id_fields = ('author', 'location')
    search_fields = ('location__city', 'author__user__first_name', 'author__user__last_name')

admin.site.register(Story, StoryAdmin)
