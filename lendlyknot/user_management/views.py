from django.shortcuts import get_object_or_404, render, redirect
from .forms import  UpdateProductForm, UserProfileForm, UserRegistrationForm, ShopRegistrationForm, AddProductForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . models import CustomUser, Product, ShopProfile


def home(request):
   products = Product.objects.all()
   return render(request, 'index.html',{'products':products})

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



def shopdashboard(request):
    shop_id = request.session.get('shop_id')
    #shop_instance = ShopProfile.objects.get(id=shop_id)
    #products = Product.objects.get(shop_id=shop_id)
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
