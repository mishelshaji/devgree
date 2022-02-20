from django.urls import path
from .views import *

urlpatterns = [
    path('<id>', home, name='classroom_home'),
    path('join/', join_classroom, name='classroom_join'),
]