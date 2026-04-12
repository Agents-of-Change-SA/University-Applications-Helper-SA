from rest_framework import serializers

from .models import UserDetails


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['id', 'name', 'surname', 'age', 'career_aspiration']
        read_only_fields = ['id']
