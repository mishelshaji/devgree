from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('contact/', ContactUsCreateView.as_view(), name='contact'),
    path('noticeboard/', NoticeboardListView.as_view(), name='noticeboard'),
    path('noticeboard/<int:id>/', NoticeboardDetailView.as_view(), name='noticeboard_detail'),
]
