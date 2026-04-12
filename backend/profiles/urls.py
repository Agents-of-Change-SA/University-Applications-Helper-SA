from django.urls import path

from .views import UserDetailsView

urlpatterns = [
    path('user-details/', UserDetailsView.as_view(), name='user-details'),
]
