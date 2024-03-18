import json
from django.conf import settings
from django.dispatch import receiver
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .tasks import send_payment_success_email
from .constants import PaymentStatus
from .models import Checkout
from user_management .models import Booking, CustomUser, Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import razorpay


# Create your views here.

def checkout(request, pk):
    instance = get_object_or_404(Booking, pk=pk)
    
    # Access the product name through the ForeignKey relationship
    product = instance.product 
    return render(request, 'payment/checkout.html', {'instance': instance, 'product': product})

def order_payment(request):
    if request.method == 'POST':
        #print("POST data:", request.POST)
        booking_id = request.POST.get("booking")
        booking = get_object_or_404(Booking, id=booking_id)
        user_id = request.POST.get("user")
        user = get_object_or_404(CustomUser, id=user_id)
        product_id = request.POST.get("product")
        product = get_object_or_404(Product, id=product_id)
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        Country = request.POST.get("Country")
        Address = request.POST.get("StreetAddress")
        Apartment = request.POST.get("Apartment")
        TownCity = request.POST.get("Town")
        State = request.POST.get("Country")
        Postcode = request.POST.get("Postcode")
        Phone = request.POST.get("Phone")
        Email = request.POST.get("Email")
        amount = float(request.POST.get("amount"))
         
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )

        order = Checkout.objects.create(
            booking=booking, user=user, product=product, FirstName=first_name, amount=amount, LastName=last_name, Country=Country, StreetAddress=Address,
            Apartment=Apartment, TownCity=TownCity, State=State, Pin=Postcode, Phone=Phone, Email=Email, order_id=razorpay_order["id"]
        )
        order.save()
        return render(request, "payment/payment.html",{
                "callback_url": "http://" + "127.0.0.1:8000" + "/payment/callback/",
                "razorpay_key": "rzp_test_s9Ul5PQ56uqlRB",
                "order": order,
            },
        )
    return render(request, "payment/payment.html")

@csrf_exempt      
def callback(request):
    print(request.POST)
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)
    
    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        
        signature_id = request.POST.get("razorpay_signature", "")
        order = Checkout.objects.get(order_id = provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if  verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            send_payment_success_email.delay(order.Email)
            return render(request, "payment/callback.html", context={"status": order.status, "order_id": provider_order_id})
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "payment/callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get("order_id")
        print(">>>>>>>>>>>>>>>>",provider_order_id)
        order = Checkout.objects.get(order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "payment/callback.html", context={"status": order.status})
 

 
    
   