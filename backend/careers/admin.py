from django.contrib import admin

from .models import CareerAspiration, CareerGuidanceEntry


@admin.register(CareerAspiration)
class CareerAspirationAdmin(admin.ModelAdmin):
    list_display = ('aspiration', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('aspiration',)


@admin.register(CareerGuidanceEntry)
class CareerGuidanceEntryAdmin(admin.ModelAdmin):
    list_display = ('aspiration', 'subject', 'explanation')
    list_filter = ('aspiration',)
    search_fields = ('aspiration', 'subject')
