from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.db.models import Q
from rest_framework.response import Response

from users.models import Customer, Vendor, Auth
from services.models import Menu, Order, Report, Notification

def check_user(request):
    try:
        user = Auth.objects.get(email=request.user.email.lower())
    except (Auth.DoesNotExist, AssertionError):
        raise PermissionDenied
    return user

def is_vendor(request):
    '''Validates a request is from a vendor'''
    try:
        user = Vendor.objects.get(id=request.user.id)
    except (Vendor.DoesNotExist, AssertionError):
        raise PermissionDenied
    return user

def is_customer(request):
    '''Validates a request is from a customer'''
    try:
        user = Customer.objects.get(id=request.user.id)
    except (Customer.DoesNotExist, AssertionError):
        raise PermissionDenied
    return user

def is_order_vendor_or_customer(request, pk):
    '''Validates a request is the order's owner or menu's vendor'''
    try:
        user = Order.objects.get(Q(customer=request.user) | Q(vendor=request.user), pk=pk)
    except (Order.DoesNotExist, AssertionError):
        raise PermissionDenied
    return user

def is_order_customer(request, pk):
    '''Validates a request is the order's owner'''
    try:
        user = Order.objects.get(Q(customer=request.user), pk=pk)
    except (Order.DoesNotExist, AssertionError):
        raise PermissionDenied
    return user

def is_order_vendor(request, pk):
    '''Validates a request is the order's vendor'''
    try:
        user = Order.objects.get(Q(vendor=request.user), pk=pk)
    except (Order.DoesNotExist, AssertionError):
        raise PermissionDenied
    return user

def is_menu_owner(request, pk):
    '''Validates a request is from the menu's owner'''
    try:
        user = Menu.objects.get(vendor=request.user, pk=pk)
    except (Menu.DoesNotExist, AssertionError):
        raise PermissionDenied
    return user

def can_get_report(request):
    '''Validates a request can get all reports as the owner '''
    try:
        user = Report.objects.filter(vendor=request.user)
    except (Report.DoesNotExist, AssertionError):
        raise PermissionDenied
    return user

def is_report_owner(request, pk):
    '''Validates a request is from the report's owner'''
    try:
        user = Report.objects.get(vendor=request.user, pk=pk)
    except (Report.DoesNotExist, AssertionError):
        raise PermissionDenied
    return user

def can_get_notifications(request):
    '''Validates a request can get all notifications as either the sender or receiver'''
    try:
        user = Notification.objects.filter(Q(sender=request.user.first_name.title()) | Q(receiver=request.user.first_name.title()))
    except (Notification.DoesNotExist, AssertionError):
        raise PermissionDenied
    return user

def is_notification_owner(request, pk):
    '''Validates a request is fromthe notification's owner'''
    try:
        user = Notification.objects.get(Q(sender=request.user.first_name.title()) | Q(receiver=request.user.first_name.title()), pk=pk)
    except (Notification.DoesNotExist, AssertionError):
        raise PermissionDenied
    return user