from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

import re 

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def validate_first_name(self, first_name):
        if len(first_name) < 2:
            raise serializers.ValidationError("First name must be at least 2 characters long.")
        if not re.fullmatch(r"[A-Za-z]+([ '-][A-Za-z]+)*", first_name):
            raise serializers.ValidationError(
                "First name can only contain letters, hyphens, and spaces (e.g., 'Mary-Jane', 'Mary Jane')."
            )
        return first_name

    def validate_last_name(self, last_name):
        if len(last_name) < 2:
            raise serializers.ValidationError("Last name must be at least 2 characters long.")
        if not re.fullmatch(r"[A-Za-z]+([ '-][A-Za-z]+)*", last_name):
            raise serializers.ValidationError(
                "Last name can only contain letters, hyphens, and spaces (e.g., 'Smith-Jones', 'De la Cruz')."
            )
        return last_name    

    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', password):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return password
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name = validated_data['last_name'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

