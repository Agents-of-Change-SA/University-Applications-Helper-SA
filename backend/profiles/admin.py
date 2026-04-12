from django.contrib import admin

from .models import UserDetails


@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'age', 'career_aspiration', 'user')
    search_fields = ('name', 'surname')
