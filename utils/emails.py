from django.conf import settings
from django.core.mail import send_mail
from services.models import Order, Customer, Vendor

def register_customer(user, to_email):
    subject = "Confirm Email to FoodVen"
    message = "Hello {} {}! \nYou are trying to sign up with this email: \n{}\nKindly open this link to continue http://localhost:8000/customers/set-password/{}".format(
        user.first_name, user.last_name, user.email, user.id)
    from_email = "noreply@foodvend.com"

    send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])


def register_vendor(user, to_email):
    subject = "Confirm Email to FoodVen"
    message = "Hello {} {}! \nYou are trying to sign up as a vendor with this email: \n{}\nBusiness name: \n{}\n Kindly open this link to continue http://localhost:8000/vendors/set-password/{}".format(
        user.first_name, user.last_name, user.email, user.business_name, user.id)
    from_email = "noreply@foodvend.com"

    send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email] )


def welcome_email(to_email):
    subject = "Welcome to Foodven!"
    message = "We are happy to have you on this platform! Login to explore this platform\nhttps://localhost:8000/login/"
    from_email = "noreply@foodven.com"
    
    send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])


def order_progress(order):
    subject = 'Your order is in progress!'.format(order.vendor.business_name)
    message = 'Order ID: {}\nMenu: {}\nDescription:  {}\nAmount: {}\nVendor: {}'.format(
                order.id, order.menu.name, order.menu.description, order.amount_due, order.vendor.business_name)
    from_email = 'noreply@foodven.com'
    to_email = order.customer.email

    send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])    
    

def order_ready(order):
    subject = 'FoodVen: Your order is Ready!'
    message = 'Order ID: {}\nMenu: {}\nDescription:  {}\nAmount: {}\nVendor: {}'.format(
                order.id, order.menu.name, order.menu.description, order.amount_due, order.vendor.business_name)
    from_email = 'noreply@foodven.com'
    to_email = order.customer.email
            
    send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])


def order_cancel(order):
    subject = 'FoodVen: Your order was cancelled!'
    message = 'Order ID: {}\nMenu: {}\nDescription:  {}\nAmount: {}\nVendor: {}'.format(
                order.id, order.menu.name, order.menu.description, order.amount_due, order.vendor.business_name)
    from_email = 'noreply@foodven.com'
    to_email = order.customer.email
            
    send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])
