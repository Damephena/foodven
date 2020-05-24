from django.db import models
from django.db.models import Avg, Count, Min, Sum, Max
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

from users.models import Auth, Customer, Vendor

# Create your models here.
class Menu(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=400)
    description = models.TextField(default="No description",blank=True)
    price = models.FloatField(default=0.00)
    quantity = models.IntegerField(default=1)
    is_recurring = models.BooleanField(default=False)
    # frequency_of_reoccurence = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + 'vendor: ' + self.vendor.business_name
    

class OrderStatus(models.Model):

    NAMES = [
        ('ready', 'ready'),
        ('progress', 'progress'),
        ('pending', 'pending'),
        ('cancelled', 'cancelled')
    ]
    name = models.CharField(max_length=20, choices=NAMES, default='pending')

    class Meta:
        verbose_name = _('order status')
        verbose_name_plural = _('order statuses')


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, default=None)
    amount_due = models.FloatField()
    amount_paid = models.FloatField(default=0.00, blank=True)
    amount_outstanding = models.FloatField(default=0.00, blank=True)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    is_preorder = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    expected_date = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.menu.name + "\n ordered by:" + self.customer.first_name


class Report(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    total_paid = models.FloatField()
    total_outstanding = models.FloatField(default=0)
    total_menus = models.IntegerField()
    total_oweing_customers = models.IntegerField()
    total_paid_customers = models.IntegerField()
    total_customers = models.IntegerField()
    total_orders = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor.business_name


class MessageStatus(models.Model):
    STATUSES = [
        ('sent', 'sent'),
        ('pending', 'pending'),
        ('not sent', 'not sent')
    ]
    name = models.TextField(default='not sent', choices=STATUSES)

    class Meta:
        verbose_name = _('message status')
        verbose_name_plural = _('message statuses')


class Notification(models.Model):
    sender = models.CharField(max_length=250)
    receiver = models.CharField(max_length=250)
    message = models.TextField()
    message_status = models.ForeignKey(MessageStatus, on_delete=models.CASCADE, related_name='notification_status')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject_user + ":\n"+ self.message
    