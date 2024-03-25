from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver 
from user_management.models import Booking 
from django.db.models.fields import CharField
from .constants import PaymentStatus
from user_management.models import CustomUser, Product, Booking


class Checkout(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    FirstName = models.CharField(max_length=255)
    LastName = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Country = models.CharField(max_length=255)
    StreetAddress = models.CharField(max_length=255)
    Apartment = models.CharField(max_length=255)
    TownCity  = models.CharField(max_length=255)
    State = models.CharField(max_length=255)
    Pin = models.IntegerField()
    Phone = models.IntegerField()
    Email = models.EmailField()
    status = CharField(("Payment Status"), default=PaymentStatus.PENDING,max_length=254,blank=False,null=False,)
    order_id = models.CharField(max_length=100,blank=True)
    payment_id = models.CharField(max_length=100,blank=True)
    signature_id = models.CharField(max_length=100,blank=True)
