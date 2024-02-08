
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Product, ShopProfile, UserProfile

class UserRegistrationForm(UserCreationForm):
   
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class ShopRegistrationForm(forms.ModelForm):
    
    class Meta:
        model = ShopProfile
        exclude = ['user'] 
        
class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        exclude = ['user'] 

   
class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['shop_id']

class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['shop_id']


        
 