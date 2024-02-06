from django.shortcuts import render, redirect
from .forms import UserProfileForm, UserRegistrationForm, ShopRegistrationForm 
from django.contrib.auth import authenticate, login
from django.contrib import messages
from . models import CustomUser, Product


def home(request):
    #View for rendering the home page.
    return render(request, 'index.html')

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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
     
        if user is not None:
            login(request, user)
            #Checking users based on roles
            if user.role == 'shop_owner':
                return redirect('home')  
            else:
                return redirect('home')  
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'user_management/login.html',{'user': request.user})
