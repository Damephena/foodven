"""This module performs query calculations for populating Report Model"""

import pytz
import datetime

from django.db.models import Q, Sum, Count
from rest_framework.response import Response

from services.models import Order, Report
from users.models import Vendor
import services.serializers as serializers
from utils.email import generate_daily_report

def get_or_generate_report(vendor):
    """Generates report only once"""
    
    day = datetime.datetime.today().replace(tzinfo=pytz.UTC).day
    try:
        report = Report.objects.filter(Q(created_at__day=day))

        if not report:
            raise Report.DoesNotExist
        else:
            serializer = serializers.ReportSerializer(report, many=True)
            return serializer.data
    except (Report.DoesNotExist):
        order = Order.objects.filter(vendor=vendor)
        day = datetime.datetime.today().replace(tzinfo=pytz.UTC).day

        paid_sum = order.filter(created_at__day=day).aggregate(Sum('amount_paid'))
        outstanding_sum = order.filter(created_at__day=day).aggregate(Sum('amount_outstanding'))
        menu_sum =  order.filter(created_at__day=day).aggregate(Count('menu'))
        oweing_customers = order.filter(amount_outstanding__gt=0, created_at__day=day).aggregate(Count('customer', distinct=True))
        paid_customers = order.filter(amount_outstanding__lte=0, created_at__day=day).aggregate(Count('customer', distinct=True))
        all_customers = order.filter(created_at__day=day).aggregate(Count('customer', distinct=True))
        all_orders = order.filter(created_at__day=day).aggregate(Count('menu'))
        # top_menus = order.filter(created_at__day=day).values('menu').annotate(menu_count=Count('menu')).order_by('-menu_count')
        
        total_paid = paid_sum['amount_paid__sum']
        total_outstanding = outstanding_sum['amount_outstanding__sum']
        total_menus = menu_sum['menu__count']
        # popular_menu = top_menus.first()
        total_oweing_customers = oweing_customers['customer__count']
        total_paid_customers = paid_customers['customer__count']
        total_customers = all_customers['customer__count']
        total_orders = all_orders['menu__count']

        data = {
            'vendor' : vendor,
            'total_paid' : paid_sum['amount_paid__sum'],
            'total_outstanding' : outstanding_sum['amount_outstanding__sum'],
            'total_menus' : menu_sum['menu__count'],
            'total_oweing_customers' : oweing_customers['customer__count'],
            'total_paid_customers' : paid_customers['customer__count'],
            'total_customers' : all_customers['customer__count'],
            'total_orders' : all_orders['menu__count'],
        }
        
        serializer = serializers.ReportSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            generate_daily_report(
                vendor,
                total_paid,
                total_outstanding,
                total_menus,
                total_oweing_customers,
                total_paid_customers,
                total_customers,
                total_orders
                )
            return serializer.data
        
    