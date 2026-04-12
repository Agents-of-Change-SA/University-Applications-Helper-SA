from django.urls import path

from .views import SchoolProfileView

urlpatterns = [
    path('school-profile/', SchoolProfileView.as_view(), name='school-profile'),
]
