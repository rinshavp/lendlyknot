from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task
def send_payment_success_email(mail_details):
    user_mail = mail_details['user_mail']
    shop_user_email = mail_details['shop_user_email']

    mail_details = {
        'order_id': mail_details['order_id'],
        'booked_date': mail_details['booked_date'],
        'amount': mail_details['amount'],
        'start_date': mail_details['start_date'],
        'end_date': mail_details['end_date'],
        'user': mail_details['user_name'],
        'shop_name': mail_details['shop_name'],
        'no_of_days': mail_details['no_of_days'],
    }
    # Render the HTML email template for customer with context variables
    customer_html_message = render_to_string('payment/customer_success_email.html', mail_details)
    
    # Send the email to customer
    send_mail(
        'Payment Successful',
        '',  # Leave the message empty, as it's included in the HTML content
        'rinshavp2000@gmail.com',
        [user_mail],
        html_message=customer_html_message  # Pass the HTML message
    )

    #Render the HTML email template for shop user with context variables
    shop_user_html_message = render_to_string('payment/shop_success_email.html', mail_details)
    
    # Send the email to shop user
    send_mail(
        'New Order Placed',
        '',  # Leave the message empty, as it's included in the HTML content
        'rinshavp2000@gmail.com',
        [shop_user_email],
        html_message=shop_user_html_message  # Pass the HTML message
    )