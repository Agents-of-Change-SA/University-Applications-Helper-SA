from django.contrib import admin
from .models import CustomUser, ChooseSubjects, ComputeAPS, GetCourses

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(ChooseSubjects)

class ComputeAPSAdmin(admin.ModelAdmin):
    readonly_fields = ('APS', 'Average', 'FPS', 'WPS')

    # Display calculated APS in admin
    def APS(self, obj):
        try:
            return obj.get_user_subjects() or 0
        except:
            return 0

    # Display calculated Average in admin
    def Average(self, obj):
        try:
            return obj.set_average() or 0
        except:
            return 0
admin.site.register(ComputeAPS, ComputeAPSAdmin)

class GetCoursesAdmin(admin.ModelAdmin):
    list_display = ('Courses',)
    readonly_fields = ('Courses',)

    def retrieved_courses(self, obj):
        return obj.retrieve_courses()

# def get_queryset(self, request):
#     qs = super().get_queryset(request)
#     for obj in qs:
#         obj.Courses = obj.retrievecourses()
#     return qs

admin.site.register(GetCourses, GetCoursesAdmin)

