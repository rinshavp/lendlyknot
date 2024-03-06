from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import  Checkout

class CheckoutForm(UserCreationForm):
   
    class Meta:
        model = Checkout
        fields = ['FirstName', 'LastName', 'amount']