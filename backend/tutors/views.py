from rest_framework.viewsets import ReadOnlyModelViewSet

from .filtersets import TutorFilterSet
from .models import Tutor
from .serializers import TutorSerializer


class TutorViewSet(ReadOnlyModelViewSet):
    """
    GET /api/tutors/      — list tutors (filterable by subject, searchable by name)
    GET /api/tutors/{id}/ — retrieve a tutor
    """
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    filterset_class = TutorFilterSet
    search_fields = ['name']
    ordering_fields = ['name', 'subject']
