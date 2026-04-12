from django.urls import path

from .views import (
    CareerAspirationDetailView,
    CareerAspirationListCreateView,
    CareerGuidanceView,
)

urlpatterns = [
    path('career-aspirations/', CareerAspirationListCreateView.as_view(), name='career-aspirations-list'),
    path('career-aspirations/<int:pk>/', CareerAspirationDetailView.as_view(), name='career-aspirations-detail'),
    path('career-guidance/', CareerGuidanceView.as_view(), name='career-guidance'),
]
