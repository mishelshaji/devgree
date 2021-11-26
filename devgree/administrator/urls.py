from django.urls import path
from .views import *

urlpatterns = [
    path('', admin_home, name='admin_home'),
    path('department/', DepartmentListView.as_view(), name='department_list'),
    path('department/create/', DepartmentCreateView.as_view(), name='department_create'),
    path('course/', CourseListView.as_view(), name='course_list'),
    path('course/create/', CourseCreateView.as_view(), name='course_create'),
]