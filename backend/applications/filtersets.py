import django_filters

from .models import ApplicationEntry


class ApplicationEntryFilterSet(django_filters.FilterSet):
    institution_name = django_filters.CharFilter(
        field_name='institution_name', lookup_expr='icontains',
    )
    open_date_from = django_filters.DateFilter(
        field_name='open_date', lookup_expr='gte',
    )
    open_date_to = django_filters.DateFilter(
        field_name='open_date', lookup_expr='lte',
    )
    close_date_from = django_filters.DateFilter(
        field_name='close_date', lookup_expr='gte',
    )
    close_date_to = django_filters.DateFilter(
        field_name='close_date', lookup_expr='lte',
    )
    min_fee = django_filters.NumberFilter(
        field_name='application_fee', lookup_expr='gte',
    )
    max_fee = django_filters.NumberFilter(
        field_name='application_fee', lookup_expr='lte',
    )

    class Meta:
        model = ApplicationEntry
        fields = [
            'institution_name',
            'open_date_from',
            'open_date_to',
            'close_date_from',
            'close_date_to',
            'min_fee',
            'max_fee',
        ]
