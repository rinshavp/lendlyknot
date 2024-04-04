from django.contrib import admin
from .models import Booking, Category, CustomUser, ShopProfile, UserProfile, Product, Wishlist
admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(ShopProfile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Booking)
admin.site.register(Wishlist)