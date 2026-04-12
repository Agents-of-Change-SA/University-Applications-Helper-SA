from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserDetails
from .serializers import UserDetailsSerializer


class UserDetailsView(APIView):
    """
    GET  /api/user-details/  — retrieve current user's details
    POST /api/user-details/  — create details
    PATCH /api/user-details/ — partial update
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            details = request.user.details
        except UserDetails.DoesNotExist:
            return Response(
                {'detail': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = UserDetailsSerializer(details)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserDetailsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        try:
            details = request.user.details
        except UserDetails.DoesNotExist:
            return Response(
                {'detail': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = UserDetailsSerializer(
            details, data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
