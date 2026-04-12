from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SchoolProfile
from .serializers import SchoolProfileSerializer, SchoolProfileWriteSerializer


class SchoolProfileView(APIView):
    """
    GET  /api/school-profile/ — retrieve
    POST /api/school-profile/ — create or update
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.school_profile
        except SchoolProfile.DoesNotExist:
            return Response(
                {'detail': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = SchoolProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        serializer = SchoolProfileWriteSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response(
            SchoolProfileSerializer(profile).data,
            status=status.HTTP_200_OK,
        )
