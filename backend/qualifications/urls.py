from rest_framework.routers import DefaultRouter

from .views import InstitutionViewSet, QualificationViewSet

router = DefaultRouter()
router.register('institutions', InstitutionViewSet, basename='institution')
router.register('qualifications', QualificationViewSet, basename='qualification')

urlpatterns = router.urls
