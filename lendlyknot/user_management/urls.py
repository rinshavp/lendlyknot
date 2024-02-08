from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user_registration/', views.user_registration, name='user_registration'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('shopregistration/', views.shop_registration, name='shopregistration'),
    path('shopdashboard/', views.shopdashboard, name='shopdashboard'),
    path('add_product/', views.add_product, name='add_product'),
    path('products/<int:pk>/update/', views.update_product, name='update_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
    
    
]

