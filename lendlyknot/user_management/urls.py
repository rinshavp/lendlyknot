from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user_registration/', views.user_registration, name='user_registration'),
    path('login/', views.custom_login, name='login'),
    path('shopregistration/', views.shop_registration, name='shopregistration'),
]

