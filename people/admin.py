from django.contrib import admin
from models import Author, Organizer


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'occupation', 'employer', 'anonymous')
    list_filter = ('anonymous',)
    search_field = ('user__firstname', 'user__lastname')

admin.site.register(Author, AuthorAdmin)
admin.site.register(Organizer)
