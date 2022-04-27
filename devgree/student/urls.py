from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='student_home'),
    path('notice/', notice, name='student_notice'),
    path('notice/<int:id>/', notice_view, name='student_notice_view'),
]