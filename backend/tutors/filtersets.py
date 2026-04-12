import django_filters

from .models import Tutor


class TutorFilterSet(django_filters.FilterSet):
    subject = django_filters.CharFilter(
        field_name='subject', lookup_expr='icontains',
    )

    class Meta:
        model = Tutor
        fields = ['subject']
