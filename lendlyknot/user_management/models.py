from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER = 'user'
    SHOP_OWNER = 'shop_owner'
    ROLE_CHOICES = [
        (USER, 'User'),
        (SHOP_OWNER, 'Shop Owner'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER)

class UserProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=15)
    house_name = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pin = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class ShopProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=255)
    shop_description = models.TextField()
    registration_number = models.CharField(max_length=255,unique=True)
    locality = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pin = models.CharField(max_length=10)
    

    def __str__(self):
        return self.shop_name

class Category(models.Model):
    category_name = models.CharField(max_length=200)
    category_code = models.CharField(max_length=255,unique=True , default=1)
    desc = models.TextField()
     
    def __str__(self):
        return self.category_name

class Product(models.Model):
    shop_id = models.ForeignKey(ShopProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    desc = models.TextField()
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    availability_status = models.BooleanField(default=True)
    product_image = models.ImageField(upload_to='product_image/')
    
    def __str__(self):
        return self.product_name





