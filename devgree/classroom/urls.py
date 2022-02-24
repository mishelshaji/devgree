from django.urls import path
from .views import *

urlpatterns = [
    path('<id>', home, name='classroom_home'),
    path('<id>/students/', students, name='classroom_students'),
    path('<id>/teachers/', teachers, name='classroom_teachers'),
    path('join/', join_classroom, name='classroom_join'),
]