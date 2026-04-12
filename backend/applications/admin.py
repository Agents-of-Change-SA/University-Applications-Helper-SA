from django.contrib import admin

from .models import ApplicationEntry


@admin.register(ApplicationEntry)
class ApplicationEntryAdmin(admin.ModelAdmin):
    list_display = (
        'institution_name',
        'open_date',
        'close_date',
        'application_fee',
        'portal_url',
    )
    list_filter = ('open_date', 'close_date')
    search_fields = ('institution_name',)
