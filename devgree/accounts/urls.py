from django.urls import path
from .views import *

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/edit', UpdateProfileView.as_view(), name='edit_profile'),
    path('password/update', password_update, name='password_update'),
]