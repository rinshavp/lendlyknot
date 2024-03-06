from collections import defaultdict
import json
from django.http import  JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .serializers import BookingSerializer
from .forms import  UpdateProductForm, UserProfileForm, UserRegistrationForm, ShopRegistrationForm, AddProductForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . models import Booking, CustomUser, Product, ShopProfile
from rest_framework.decorators import api_view
from datetime import date, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

def home(request):
   products = Product.objects.order_by('-created_at')[:8]
   return render(request, 'index.html',{'products':products})

#------------------------------USER AUTHENTICATION-------------------------------

def user_registration(request):

    #View for handling user registration.
    # Check if the form is submitted using POST method
    if request.method == 'POST':
        # Create instances of UserRegistrationForm and UserProfileForm with the submitted POST data
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        # Check if both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User model instance with the role set to 'user'
            user_instance = user_form.save(commit=False)
            user_instance.role = CustomUser.USER
            user_instance.save()

            # Save UserProfile model instance with the associated user
            profile_instance = profile_form.save(commit=False)
            profile_instance.user = user_instance
            profile_instance.save()

            
            return redirect('home')  # Redirect to a home page

    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'user_management/user_registration.html', {'user_form': user_form, 'profile_form': profile_form})

def shop_registration(request):
    # Check if the form is submitted using POST method
    if request.method == 'POST':
        # Create instances of UserRegistrationForm and ShopRegistrationForm with the submitted POST data
        user_form = UserRegistrationForm(request.POST)
        shop_form = ShopRegistrationForm(request.POST)

        # Check if both forms are valid
        if user_form.is_valid() and shop_form.is_valid():
            # Save User model instance with the role set to 'shop_owner'
            user_instance = user_form.save(commit=False)
            user_instance.role = CustomUser.SHOP_OWNER
            user_instance.save()

            # Save Shop model instance with the associated shop_owner
            shop_instance = shop_form.save(commit=False)
            shop_instance.user = user_instance
            shop_instance.save()

            # Redirect to the home page after successful registration
            return redirect('home')

    else:
        user_form = UserRegistrationForm()
        shop_form = ShopRegistrationForm()

    return render(request, 'user_management/shop_registration.html', {'user_form': user_form, 'shop_form': shop_form})

def custom_login(request):
    #Check if the form is being submitted (POST request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
     
        if user is not None:
            request.session['user_name'] = user.username 
            request.session['user_id'] = user.id
            login(request, user)

            if user.role == 'shop_owner':
                shop = ShopProfile.objects.get(user=user)
                request.session['shop_id'] = shop.id
                return redirect('shopdashboard')  # Replace with your shop owner dashboard URL
            else:
                return redirect('home')  # Replace with your user dashboard URL
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'user_management/login.html',{'user': request.user})


def logout_view(request):
    logout(request)
    request.session.flush()  # or request.session.clear()
    return redirect('home')

#--------------------------SHOP FUNCTIONALITIES-----------------------------------------------------

def shopdashboard(request):
    #Retrieve shop_id for the current shop
    shop_id = request.session.get('shop_id')
    #Displaying product based on the shop_id
    products = Product.objects.filter(shop_id=shop_id)
    
    return render(request, 'shop_owner/shop_dashboard.html',{'products':products,})

def add_product(request):
    #Check if the form is being submitted (POST request)
    if request.method == 'POST':
        form = AddProductForm(request.POST,request.FILES)
        if form.is_valid():
            # Retrieve shop ID from session
            shop_id = request.session.get('shop_id')
                 
            shop_instance = ShopProfile.objects.get(id=shop_id)
            product = form.save(commit=False)
            product.shop_id =shop_instance
            product.save()

            
            return redirect('shopdashboard')  # Redirect to the login page after successful registration
    else:
        form = AddProductForm()

    return render(request, 'shop_owner/add_product.html', {'form': form})

def update_product(request, pk):
    #Retrieve the product instance with the given primary key (pk)
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        #Create a form instance with the submitted data and the existing product instance
        form = UpdateProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('shopdashboard')  # Redirect to product detail view
    else:
        form = UpdateProductForm(instance=product)

    return render(request, 'shop_owner/update_product.html', {'form': form})

def delete_product(request, pk):
    #  Retrieve the product instance with the given primary key (pk)
    product = get_object_or_404(Product, pk=pk)
    
    #  Check if the request is a POST request
    if request.method == 'POST':
        #  Delete the product from the database
        product.delete()
        
        #  Redirect to a view or URL after successful deletion
        return redirect('shopdashboard')  # Redirect to product list view
    
    #  Render a confirmation page for deletion (delete_product.html)
    return render(request, 'shop_owner/delete_product.html', {'product': product})

def shop_product(request):
    products = Product.objects.all()
    return render(request, 'user_management/shop.html', {'products':products})

#------------------------BOOKING-------------------------------------------------------


@api_view(['POST'])
def ProductBooking(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        #serializer.save()
        instance = serializer.save()
        #return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Assuming the instance has an 'id' field you want to use to show details
        return Response({'redirect_url': f'/payment/checkout/{instance.id}/'})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         

def display_sizes(request, pk):
    
    # Assuming you have a product_id to identify the product
    product = get_object_or_404(Product,pk=pk)
    # Fetch available sizes for the product where quantity is greater than zero
    available_sizes = {}
    size_quantities = [product.size_s_qty, product.size_m_qty, product.size_l_qty,
                   product.size_xl_qty, product.size_xxl_qty, product.size_xxxl_qty]
    size_mapping = ['S', 'M', 'L', 'XL', 'XXL', 'XXXL']

    for i, qty in enumerate(size_quantities, start=1):
        if qty > 0:
            available_sizes[str(i)] = size_mapping[i-1]

# Now, available_sizes is a dictionary with keys '1' to '6' representing sizes S to XXXL with corresponding values.

    # Add more sizes as needed...

    context = {
        'product': product,
        'available_sizes': available_sizes,
    }
    return render(request, 'bookings/product_details.html', context)
    #return render(request, 'bookings/product_booking.html', context)

#class based view

class DateInfoView(APIView):
    def get(self, request, product_id, size_id ):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        
        bookings = Booking.objects.filter(product = product_id, booked_size = size_id, booking_status__in=[1, 4] )
        date_quantities = defaultdict(int)
        
        for booking in bookings:
            delta = (booking.end_date - booking.start_date).days + 1
            for i in range(delta):
                day = booking.start_date + timedelta(days=i)
                date_quantities[day] += booking.quantity_rented
        
        size_mapping = {
            1: 'size_s_qty',
            2: 'size_m_qty',
            3: 'size_l_qty',
            4: 'size_xl_qty',
            5: 'size_xxl_qty',
        }

        product_total_quantity = getattr(product, size_mapping.get(size_id, 'size_xxxl_qty'))
        #Determine which dates are fully booked
        fully_booked_dates = [str(day) for day, quantity in date_quantities.items() if quantity >= product_total_quantity]
        
        return JsonResponse({'fully_booked_dates': fully_booked_dates})




            