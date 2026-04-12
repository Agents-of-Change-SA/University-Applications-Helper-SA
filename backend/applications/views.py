from rest_framework.viewsets import ModelViewSet

from .filtersets import ApplicationEntryFilterSet
from .models import ApplicationEntry
from .serializers import ApplicationEntrySerializer


class ApplicationEntryViewSet(ModelViewSet):
    """
    CRUD for application date entries.
    Supports filtering, search, and ordering per the swagger spec.
    """
    queryset = ApplicationEntry.objects.all()
    serializer_class = ApplicationEntrySerializer
    filterset_class = ApplicationEntryFilterSet
    search_fields = ['institution_name']
    ordering_fields = [
        'institution_name',
        'open_date',
        'close_date',
        'application_fee',
    ]
