from django.urls import include, path
from .views import CreateUser, ChooseSubjectsView, ComputeAPSView, GetCoursesView

urlpatterns = [
    path('users/', CreateUser.as_view(), name='user_create'),
    path('stream/', ChooseSubjectsView.as_view(), name="stream"),
    path('computeaps/', ComputeAPSView.as_view(), name='computeaps'),
    path('getcourses/', GetCoursesView.as_view(), name="get_courses")
 ]