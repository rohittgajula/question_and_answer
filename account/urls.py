from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('all_users/', views.all_user, name='all_users'),
    path('me/', views.get_user, name='me'),
    path('me/update/', views.update_user, name='update_user'),
]