from django.urls import path
from . import views

urlpatterns = [
    path('keywords/', views.get_keywords, name='get_keywords'),
    path('keywords/update/', views.update_keywords, name='update_keywords'),
    path('users/', views.get_users, name='get_users'),
    path('users/update/', views.update_users, name='update_users'),
    path('serverStatus/', views.get_server_status, name='get_server_statu'),
    path('serverStatus/update/', views.update_server_status, name='update_server_status')
]
