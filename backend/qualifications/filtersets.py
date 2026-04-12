import django_filters

from .models import Institution, Qualification


class InstitutionFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains',
    )

    class Meta:
        model = Institution
        fields = ['name']


class QualificationFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains',
    )
    institution = django_filters.NumberFilter(
        field_name='institution_id',
    )
    institution_name = django_filters.CharFilter(
        field_name='institution__name', lookup_expr='icontains',
    )
    faculty = django_filters.CharFilter(
        field_name='faculty', lookup_expr='icontains',
    )
    min_aps = django_filters.NumberFilter(
        field_name='minimum_aps', lookup_expr='gte',
    )
    max_aps = django_filters.NumberFilter(
        field_name='minimum_aps', lookup_expr='lte',
    )

    class Meta:
        model = Qualification
        fields = [
            'name', 'institution', 'institution_name',
            'faculty', 'min_aps', 'max_aps',
        ]
