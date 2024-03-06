from django.urls import path
from . import views
from .views import DateInfoView, ProductBooking

urlpatterns = [
    path('', views.home, name='home'),
    path('user_registration/', views.user_registration, name='user_registration'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('shop_registration/', views.shop_registration, name='shop_registration'),
    path('shopdashboard/', views.shopdashboard, name='shopdashboard'),
    path('add_product/', views.add_product, name='add_product'),
    path('products/<int:pk>/update/', views.update_product, name='update_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('shop_product/', views.shop_product, name='shop_product'),
    path('display_sizes/<int:pk>/', views.display_sizes, name='display_sizes'),
    path('get_dates/<int:product_id>/<int:size_id>/', DateInfoView.as_view(), name='get_dates'),
    path('product_booking/', views.ProductBooking, name='product_booking'),
]



