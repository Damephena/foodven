from django.db import models
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
        ('in progress', 'in progress'),
        ('pending', 'pending'),
        ('cancelled', 'cancelled')
    ]
    name = models.CharField(max_length=400)

    class Meta:
        verbose_name = _('order status')
        verbose_name_plural = _('order statuses')


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    description = models.TextField(default="No description", blank=True)
    items_ordered = models.ManyToManyField(Menu, blank=True)
    amount_due = models.FloatField()
    amount_paid = models.FloatField(default=0.00)
    amount_outstanding = models.FloatField(default=amount_due)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description + "\n ordered by:" + self.customer_id.first_name
    

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
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='notification_order')
    message_status = models.ForeignKey(MessageStatus, on_delete=models.CASCADE, related_name='notification_status')
    created_at = models.DateTimeField(auto_now_add=True)

    def email_user(self,  subject, message, from_email=None, *args, **kwargs):
        ''' Sends an email to this User '''
        send_mail(subject, message, from_email, [*args], **kwargs)

    def __str__(self):
        return self.subject_user + ":\n"+ self.message
    