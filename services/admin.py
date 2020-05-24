from django.contrib import admin
from .models import Menu, Order, OrderStatus, Report, Notification, MessageStatus
# Register your models here.

admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(OrderStatus)
admin.site.register(Notification)
admin.site.register(MessageStatus)
admin.site.register(Report)