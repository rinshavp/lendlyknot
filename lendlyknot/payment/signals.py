from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, render
from .tasks import send_payment_success_email
from .constants import PaymentStatus
from .models import Checkout
from user_management.models import Booking


@receiver(post_save, sender=Checkout)
def update_booking_status(sender, instance, **kwargs):
    if instance.status == PaymentStatus.SUCCESS:
        booking = instance.booking
        booking.booking_status = '1'
        booking.save()
        mail_details = {}

         # Trigger the Celery task to send email asynchronously
        send_payment_success_email.delay(mail_details)

        