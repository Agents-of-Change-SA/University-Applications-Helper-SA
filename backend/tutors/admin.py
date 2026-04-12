from django.contrib import admin

from .models import Tutor


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'contact')
    list_filter = ('subject',)
    search_fields = ('name', 'subject')
