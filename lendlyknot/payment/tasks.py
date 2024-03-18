from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string

@shared_task
def send_payment_success_email(email):
    # Context data to be passed to the email template
    context = {
        'message': 'Your payment was successful. Thank you for your purchase!'
    }
    
    # Render the HTML email template with context variables
    html_message = render_to_string('payment/payment_success_email.html', context)
    
    # Send the email
    send_mail(
        'Payment Successful',
        '',  # Leave the message empty, as it's included in the HTML content
        'rinshavp2000@gmail.com',
        [email],
        html_message=html_message  # Pass the HTML message
    )