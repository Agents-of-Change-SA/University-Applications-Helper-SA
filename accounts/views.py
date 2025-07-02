from django.shortcuts import render
from .serializers import CustomUserSerializer, ChooseSubjectsSerializer, ComputeAPSSerializer, GetCoursesSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from .models import ChooseSubjects, ComputeAPS, GetCourses
from django.http import JsonResponse

# # Create your views here.
class CreateUser(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = CustomUserSerializer

class ChooseSubjectsView(generics.RetrieveAPIView):
    def get_queryset(self):
        queryset=ChooseSubjects.objects.filter(id=self.kwargs["pk"])
        return queryset
    serializer_class = ChooseSubjectsSerializer

class ComputeAPSView(generics.RetrieveAPIView):
    def get_queryset(self):
        queryset=ComputeAPS.objects.filter(id=self.kwargs["pk"])
        return queryset
    serializer_class = ComputeAPSSerializer

class GetCoursesView(generics.RetrieveAPIView):
    def get_queryset(self):
        queryset=GetCourses.objects.filter(id=self.kwargs["pk"])
        return queryset
    serializer_class = GetCoursesSerializer