import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .constants import PaymentStatus
from .models import Checkout
from user_management .models import Booking
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import razorpay


# Create your views here.

def checkout(request, pk):
    instance = get_object_or_404(Booking, pk=pk)
    
    # Access the product name through the ForeignKey relationship
    product_name = instance.product.product_name  
    return render(request, 'payment/checkout.html', {'instance': instance, 'product_name': product_name})

def order_payment(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        amount = float(request.POST.get("amount"))
         
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )

        order = Checkout.objects.create(
            FirstName=first_name, amount=amount, order_id=razorpay_order["id"]
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
            return render(request, "payment/callback.html", context={"status": order.status})
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "payment/callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get("order_id")
        order = Checkout.objects.get(order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "payment/callback.html", context={"status": order.status})