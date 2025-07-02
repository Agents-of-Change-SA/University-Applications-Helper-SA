from django.urls import path
from .views import InstitutionView, FacultyView, CourseView, SchoolView, SubjectChoicesView

urlpatterns = [
    path('institution/<int:pk>', InstitutionView.as_view(), name='institution'),
    path('faculty/<int:pk>', FacultyView.as_view(), name='faculty'),
    path('course/<int:pk>', CourseView.as_view(), name='course'),
    path('school/<int:pk>', SchoolView.as_view, name='school'),
    path('subjects/<int:pk>', SubjectChoicesView.as_view(), name='subjects'),
    # path('levels/<int:pk>', SymbolLevelView.as_view(), name='levels')
    # path('courseRequirements/<int:pk>', CourseRequirementsView.as_view(), name='courseRequirements')
]