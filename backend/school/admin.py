from django.contrib import admin

from .models import SchoolProfile, SchoolSubject


class SchoolSubjectInline(admin.TabularInline):
    model = SchoolSubject
    extra = 1


@admin.register(SchoolProfile)
class SchoolProfileAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'user')
    search_fields = ('school_name',)
    inlines = [SchoolSubjectInline]
