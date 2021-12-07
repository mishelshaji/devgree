from django.urls import path
from .views import *

urlpatterns = [
    path('', staff_home, name='staff_home'),
]