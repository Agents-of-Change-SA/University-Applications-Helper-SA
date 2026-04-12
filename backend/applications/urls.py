from rest_framework.routers import DefaultRouter

from .views import ApplicationEntryViewSet

router = DefaultRouter()
router.register('application-dates', ApplicationEntryViewSet, basename='applicationentry')

urlpatterns = router.urls
