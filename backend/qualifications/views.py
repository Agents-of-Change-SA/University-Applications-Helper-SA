from rest_framework.viewsets import ReadOnlyModelViewSet

from .filtersets import InstitutionFilterSet, QualificationFilterSet
from .models import Institution, Qualification
from .serializers import (
    InstitutionDetailSerializer,
    InstitutionSerializer,
    QualificationListSerializer,
    QualificationSerializer,
)


class InstitutionViewSet(ReadOnlyModelViewSet):
    """
    GET /api/institutions/      — list institutions
    GET /api/institutions/{id}/ — detail with nested qualifications
    """
    queryset = Institution.objects.all()
    filterset_class = InstitutionFilterSet
    search_fields = ['name', 'abbreviation']
    ordering_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return InstitutionDetailSerializer
        return InstitutionSerializer


class QualificationViewSet(ReadOnlyModelViewSet):
    """
    GET /api/qualifications/      — list qualifications (lightweight)
    GET /api/qualifications/{id}/ — full detail with APS rules, subject reqs, selection reqs
    """
    queryset = Qualification.objects.select_related('institution').prefetch_related(
        'aps_rules__conditions',
        'subject_requirements',
        'selection_requirements',
    )
    filterset_class = QualificationFilterSet
    search_fields = ['name', 'institution__name', 'faculty']
    ordering_fields = ['name', 'minimum_aps', 'institution__name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QualificationSerializer
        return QualificationListSerializer
