from .models import CustomUser, ChooseSubjects, ComputeAPS, GetCourses
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'last_login', 'date_joined']

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

class ChooseSubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChooseSubjects
        fields = '__all__'

    name = serializers.CharField(max_length=200)
    percentage = serializers.IntegerField()
    level = serializers.IntegerField()

class ComputeAPSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputeAPS
        fields = '__all__'

    subjects = serializers.CharField(max_length=200)
    APS = serializers.IntegerField()
    FPS = serializers.IntegerField()
    WPS = serializers.IntegerField()

class GetCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetCourses
        fields = '__all__'

    Courses = serializers.CharField(max_length=10000)