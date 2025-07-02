from django.shortcuts import render
from .serializers import InstitutionSerializer, FacultySerializer, CourseSerializer, SchoolSerializer, SubjectChoicesSerializer
from rest_framework.response import Response     
from rest_framework.views import APIView
from rest_framework import generics, status
from .models import Institution, Faculty, Course, School, SubjectChoices
from django.http import JsonResponse

# Create your views here.
class InstitutionView(generics.RetrieveAPIView):
    def get_queryset(self):
        queryset=Institution.objects.filter(id=self.kwargs["pk"])
        return queryset
    serializer_class = InstitutionSerializer  

class FacultyView(generics.RetrieveAPIView):
    def get_queryset(self):
        queryset=Faculty.objects.filter(id=self.kwargs["pk"])
        return queryset
    serializer_class = FacultySerializer

class SchoolView(generics.RetrieveAPIView):
    def get_queryset(self):
        queryset = School.objects.filter(id=self.kwargs["pk"])
        return queryset
    serializer_class = SchoolSerializer

class SubjectChoicesView(generics.RetrieveAPIView):
    def get_queryset(self):
        queryset = SubjectChoices.objects.filter(id=self.kwargs["pk"])
        return queryset
    serializer_class = SubjectChoices

class CourseView(generics.RetrieveAPIView):
    def get_queryset(self):
        queryset = Course.objects.filter(id=self.kwargs["pk"])
        return queryset
    serializer_class = CourseSerializer

# class CourseRequirementsView(generics.RetrieveAPIView):
#     def get_queryset(self):
#         queryset = CourseRequirements.objects.filter(id=self.kwargs["pk"])
#         return queryset
#     serializer_class = CourseRequirements

