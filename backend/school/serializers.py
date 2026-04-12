from rest_framework import serializers

from .models import SchoolProfile, SchoolSubject


class SchoolSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolSubject
        fields = ['name', 'percentage', 'level']


class SchoolProfileSerializer(serializers.ModelSerializer):
    subjects = SchoolSubjectSerializer(many=True, read_only=True)

    class Meta:
        model = SchoolProfile
        fields = ['id', 'school_name', 'subjects']
        read_only_fields = ['id']


class SchoolProfileWriteSerializer(serializers.Serializer):
    """Accepts { name, subjects } and creates/updates the profile."""
    name = serializers.CharField(max_length=255)
    subjects = SchoolSubjectSerializer(many=True)

    def create(self, validated_data):
        user = self.context['request'].user
        subjects_data = validated_data.pop('subjects')
        profile, _ = SchoolProfile.objects.update_or_create(
            user=user,
            defaults={'school_name': validated_data['name']},
        )
        profile.subjects.all().delete()
        for subj in subjects_data:
            SchoolSubject.objects.create(profile=profile, **subj)
        return profile
