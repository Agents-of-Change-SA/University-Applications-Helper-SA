from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CareerAspiration, CareerGuidanceEntry
from .serializers import CareerAspirationSerializer


class CareerAspirationListCreateView(ListCreateAPIView):
    """
    GET  /api/career-aspirations/ — list user's aspirations
    POST /api/career-aspirations/ — create aspiration
    """
    serializer_class = CareerAspirationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CareerAspiration.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CareerAspirationDetailView(APIView):
    """
    PUT    /api/career-aspirations/{id}/ — update
    DELETE /api/career-aspirations/{id}/ — delete
    """
    permission_classes = [IsAuthenticated]

    def _get_object(self, request, pk):
        try:
            return CareerAspiration.objects.get(pk=pk, user=request.user)
        except CareerAspiration.DoesNotExist:
            return None

    def put(self, request, pk):
        obj = self._get_object(request, pk)
        if obj is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CareerAspirationSerializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        obj = self._get_object(request, pk)
        if obj is None:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CareerGuidanceView(APIView):
    """
    GET /api/career-guidance/?aspiration=Software+Engineer
    Returns subject recommendations for the given aspiration.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        aspiration = request.query_params.get('aspiration', '')
        if not aspiration:
            return Response(
                {'aspiration': ['This query parameter is required.']},
                status=status.HTTP_400_BAD_REQUEST,
            )
        entries = CareerGuidanceEntry.objects.filter(
            aspiration__iexact=aspiration,
        )
        recommendations = [
            {'subject': e.subject, 'explanation': e.explanation}
            for e in entries
        ]
        return Response({
            'aspiration': aspiration,
            'recommendations': recommendations,
        })
