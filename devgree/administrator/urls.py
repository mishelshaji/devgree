from django.urls import path
from .views import *

urlpatterns = [
    path('', admin_home, name='admin_home'),
    path('department/', DepartmentListView.as_view(), name='department_list'),
    path('department/create/', DepartmentCreateView.as_view(), name='department_create'),
    path('department/edit/<id>/', DepartmentUpdateView.as_view(), name='department_edit'),

    path('course/', CourseListView.as_view(), name='course_list'),
    path('course/create/', CourseCreateView.as_view(), name='course_create'),
    path('course/edit/<id>/', CourseUpdateView.as_view(), name='course_edit'),
    path('course/delete/<int:id>/', delete_course, name='course_delete'),

    path('student/', StudentListView.as_view(), name='student_list'),
    path('student/create/', create_student, name='student_create'),
    path('student/edit/<id>/', update_student, name='student_edit'),
    path('student/delete/<id>/', delete_student, name='student_delete'),

    path('staff/', StaffListView.as_view(), name='staff_list'),
    path('staff/create/', create_staff, name='staff_create'),
    path('staff/edit/<id>', edit_staff, name='staff_edit'),
    path('staff/delete/<id>', delete_staff, name='staff_delete'),
    
]