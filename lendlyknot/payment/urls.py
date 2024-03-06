from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'payment'

urlpatterns = [
     path('checkout/<int:pk>/', views.checkout, name='checkout'),
     path("payment/", views.order_payment, name="payment"),
     path("callback/", views.callback, name="callback"),
]

