from rest_framework import serializers
from .models import Institution, Faculty, Course, School, SubjectChoices



class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'
    
    name = serializers.CharField()
    type = serializers.CharField()

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'

    institution = InstitutionSerializer(read_only=True)
    name = serializers.CharField()

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

    faculty = FacultySerializer(read_only=True)
    name = serializers.CharField()

class SubjectChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectChoices
        field = '__all__'

    name = serializers.CharField()


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    institution = InstitutionSerializer(read_only=True)
    faculty = FacultySerializer(read_only=True)
    name = serializers.CharField()
    subjects = SubjectChoicesSerializer(many=True, read_only=False)

