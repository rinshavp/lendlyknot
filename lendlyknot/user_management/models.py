from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

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
    shop_desc = models.TextField()
    registration_number = models.CharField(max_length=255,unique=True)
    locality = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pin = models.CharField(max_length=10)
    

    def __str__(self):
        return self.shop_name

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('W', 'Women'),
        ('M', 'Men'),
        ('A', 'Accessories'),
    ]
    category_name = models.CharField(max_length=200)
    category_code = models.CharField(max_length=255,unique=True , default=1)
    desc = models.TextField()
    category_type = models.CharField(max_length=1,choices=CATEGORY_CHOICES, default='W')
     
    def __str__(self):
        return self.category_name

class Product(models.Model):
    shop_id = models.ForeignKey(ShopProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255,null=True)
    product_desc = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='product_image/')
    product_image1 = models.ImageField(upload_to='product_image/', null=True)
    product_image2 = models.ImageField(upload_to='product_image/', null=True)
    size_s_qty = models.PositiveIntegerField(default=0)
    size_m_qty = models.PositiveIntegerField(default=0)
    size_l_qty = models.PositiveIntegerField(default=0)
    size_xl_qty = models.PositiveIntegerField(default=0)
    size_xxl_qty = models.PositiveIntegerField(default=0)
    size_xxxl_qty = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    
    def __str__(self):
        return self.product_name

class Booking(models.Model):
    BOOKING_CHOICES = [
        ('1', 'Booked'),
        ('2', 'Returned'),
        ('3', 'Cancelled'),
        ('4', 'Deliverd'),
        ('5', 'Initialised'),
    ]
    SIZE_CHOICES = [
        ('1', 'S'),
        ('2', 'M'),
        ('3', 'L'),
        ('4', 'XL'),
        ('5', 'XXL'),
        ('6', 'XXXL'),
        # Add more size choices as needed
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    quantity_rented= models.PositiveIntegerField(default=1)
    booked_size = models.CharField(max_length=2,choices=SIZE_CHOICES,default=1)
    booking_status =  models.CharField(max_length=2,choices=BOOKING_CHOICES,default=5)
    booked_date = models.DateTimeField(default=timezone.now)
    no_of_days = models.PositiveIntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

