from django.contrib import admin
from models import Location, Story
from people.models import Author


class LocationAdmin(admin.ModelAdmin):
    list_display = ('city_fmt', 'county', 'state_fmt', 'story_count')
    list_filter = ('state',)
    search_fields = ('city', 'county')

admin.site.register(Location, LocationAdmin)


class EmployerFilter(admin.SimpleListFilter):
    title = 'author employer'
    parameter_name = 'employer'

    def lookups(self, request, model_admin):
        employer_set = set()
        for a in Author.objects.all():
            if a.employer:
                employer_set.add(a.employer.split(' ', 1)[0])
        return [(str(c), str(c)) for c in employer_set if c]

    def queryset(self, request, queryset):
        if self.value() or self.value() == 'None':
            return queryset.filter(author__employer__startswith=self.value())
        else:
            return queryset


class StoryAdmin(admin.ModelAdmin):
    list_display = ('excerpt', 'author_display', 'employer', 'anonymous', 'created_at')
    list_filter = (EmployerFilter, 'location__state', 'truncated')
    date_hierarchy = 'created_at'
    readonly_fields = ('truncated',)
    raw_id_fields = ('author', 'location')
    search_fields = ('location__city', 'author__user__first_name', 'author__user__last_name', 'content')

admin.site.register(Story, StoryAdmin)
