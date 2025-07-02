from django.contrib import admin
from .models import CustomUser, ChooseSubjects, ComputeAPS, GetCourses

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(ChooseSubjects)

class ComputeAPSAdmin(admin.ModelAdmin):
    readonly_fields = ('APS', 'FPS', 'WPS')

def get_queryset(self, request):
    qs = super().get_queryset(request)
    for obj in qs:
        obj.APS = obj.get_user_subjects()
    return qs

admin.site.register(ComputeAPS, ComputeAPSAdmin)

class GetCoursesAdmin(admin.ModelAdmin):
    readonly_fields = ('Courses',)

def get_queryset(self, request):
    qs = super().get_queryset(request)
    for obj in qs:
        obj.Courses = obj.retrievecourses()
    return qs

admin.site.register(GetCourses, GetCoursesAdmin)

