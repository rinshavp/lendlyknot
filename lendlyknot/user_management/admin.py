from django.contrib import admin
from .models import Category, CustomUser, ShopProfile, UserProfile, Product
admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(ShopProfile)
admin.site.register(Category)
admin.site.register(Product)