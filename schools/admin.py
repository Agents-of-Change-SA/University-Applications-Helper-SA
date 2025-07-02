from django.contrib import admin
from .models import Institution, Faculty, Course, School, SubjectChoices
# Register your models here.

class SubjectInline(admin.TabularInline):
    model = Course.Subjects.through

class CourseAdmin(admin.ModelAdmin):
    inlines = [SubjectInline]
    list_display = ('name', 'institution', 'faculty', 'school', 'aps', 'duration', 'nbt')
    search_fields = ('name', 'institution', 'faculty', 'school')

admin.site.register(SubjectChoices)
admin.site.register(Course)
admin.site.register(Institution)
admin.site.register(Faculty)
admin.site.register(School)
