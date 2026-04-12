from rest_framework import serializers

from .models import CareerAspiration


class CareerAspirationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerAspiration
        fields = ['id', 'aspiration', 'created_at']
        read_only_fields = ['id', 'created_at']


class SubjectRecommendationSerializer(serializers.Serializer):
    subject = serializers.CharField()
    explanation = serializers.CharField()


class CareerGuidanceResponseSerializer(serializers.Serializer):
    aspiration = serializers.CharField()
    recommendations = SubjectRecommendationSerializer(many=True)
