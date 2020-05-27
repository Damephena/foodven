import pytz
import datetime

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import views, viewsets, generics
from rest_framework.response import Response

from services.models import Order, Menu, OrderStatus, Report, Notification
from users.models import Customer, Vendor, Auth
import services.serializers as serializers
import utils.email as mail
from utils.report import get_or_generate_report
import utils.validator as validator
# Create your views here.

class MenuListView(generics.ListCreateAPIView):
    serializer_class = serializers.MenuSerializer
    
    def get(self, obj):
        queryset = Menu.objects.all()
        serializer = serializers.MenuSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = validator.is_vendor(request)
        data = {
                'vendor': user,
                'name': request.data['name'],
                'description': request.data['description'],
                'price': request.data['price'],
                'quantity': request.data['quantity']
            }
        serializer = serializers.MenuSerializer(
                data=data,
                context={
                    'request': request.data['is_recurring'],
                }
            )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = Menu.objects.all()
    serializer_class = serializers.MenuSerializer

    def get(self, request, pk):
        try:
            queryset = Menu.objects.get(pk=pk)
        except (ObjectDoesNotExist, AssertionError):
            return Response({'error': 'Menu with given ID not found'})
        else:
            serializer = serializers.MenuSerializer(queryset, many=False)
            return Response(serializer.data)

    def put(self, request, pk):
        user = validator.is_menu_owner(request, pk)
        data = {
                'vendor': request.user,
                'name': request.data['name'],
                'description': request.data['description'],
                'price': request.data['price'],
                'is_recurring': request.data['is_recurring'],
                'quantity': request.data['quantity']
            }
            
        serializer = serializers.MenuSerializer(user, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        user = validator.is_menu_owner(request, pk)
        if user:
            menu = Menu.objects.get(pk=pk)
            if menu.delete():
                return Response({'message': 'Menu deleted successfully!'})
        

class OrderListView(generics.ListCreateAPIView):
    serializer_class = serializers.OrderSerializer

    def get(self, request):
        queryset = Order.objects.filter(Q(customer=request.user) | Q(vendor=request.user))
        serializer = serializers.OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = validator.is_customer(request)
        menu = Menu.objects.get(id=request.data['menu'])
        amount_outstanding = menu.price - float(request.data['amount_paid'])
        if request.data['is_preorder'] == True:
            data = {
                'customer': request.user,
                'vendor': menu.vendor,
                'menu': request.data['menu'],
                'amount_due': menu.price,
                'amount_outstanding': amount_outstanding,
                'amount_paid': request.data['amount_paid'],
                'order_status': 1,
                'is_preorder' : request.data['is_preorder'],
                'expected_date': request.data['expected_date'],
                }
        else:
            data = {
                'customer': request.user,
                'vendor': menu.vendor,
                'menu': request.data['menu'],
                'amount_due': menu.price,
                'amount_outstanding': amount_outstanding,
                'amount_paid': request.data['amount_paid'],
                'order_status': 1,
            }
            
        serializer = serializers.OrderSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

class OrderDetailView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def get(self, request, pk):
        queryset = validator.is_order_vendor_or_customer(request, pk)
        serializer = serializers.OrderSerializer(queryset, many=False)
        return Response(serializer.data)


class CancelOrderView(generics.UpdateAPIView):
    lookup_field = 'pk'
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def put(self, request, pk):
        order = validator.is_order_customer(request, pk)
        time_ordered = order.created_at 
        cancel_time = datetime.datetime.now()
        time_difference = cancel_time.replace(tzinfo=pytz.timezone("Africa/Lagos")) - time_ordered
        maximum_duration= 420 # allow only 7 minutes
        
        #  check order time is less than 7 mins or order_status != "pending"
        if ( time_difference.seconds > maximum_duration
                or 
            order.order_status.get_name_display() != 'pending'
            ):
            return Response({'error': 'Order cannot be cancelled.'})
        else:
            data = {'order_status': 4}
            serializer = serializers.OrderSerializer(order, data=data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.update(order, data)
                serializer.save()

                return Response(serializer.data)
                mail.order_cancel(order)
            else:
                return Response(serializer.errors)


class OrderReadyStatusView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = Order.objects.all()
    serializer_class = serializers.OrderReadyStatusSerializer

    def get(self, request, pk):
        queryset = validator.is_order_vendor(request, pk)
        serializer = serializers.OrderReadyStatusSerializer(queryset, many=False)
        return Response(serializer.data)
    
    def put(self, request, pk):
        order = validator.is_order_vendor(request, pk)
        data = {'order_status': 4}

        serializer = serializers.OrderReadyStatusSerializer(order, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.update(order, data)
            serializer.save()

            mail.order_ready(order)
            return Response(serializer.data)
        return Response(serializer.errors)

        
class OrderProgressStatusView(generics.UpdateAPIView):
    lookup_field = 'pk'
    queryset = Order.objects.all()
    serializer_class = serializers.OrderProgressStatusSerializer

    def get(self, request, pk):
        queryset = validator.is_order_vendor(request, pk)
        serializer = serializers.OrderProgressStatusSerializer(queryset, many=False)
        return Response(serializer.data)
        
    def put(self, request, pk):
        order = validator.is_order_vendor(request, pk)
        data = {'order_status': 4}

        serializer = serializers.OrderProgressStatusSerializer(order, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.update(order, data)
            serializer.save()

            mail.order_progress(order)

            return Response(serializer.data)
        return Response(serializer.errors)


class ReportListView(generics.ListAPIView):
    serializer_class = serializers.ReportSerializer

    def get(self, request):
        queryset = validator.can_get_report(request)

        serializer = serializers.ReportSerializer(queryset, many=True)
        return Response(serializer.data)


class ReportGenerateView(generics.CreateAPIView):
    serializer_class = serializers.ReportSerializer

    def post(self, request):
        vendor = validator.is_vendor(request)

        data = get_or_generate_report(vendor)
        return Response(data)


class ReportDetailView(generics.RetrieveAPIView):
    lookup_field = 'pk'
    queryset = Report.objects.all()
    serializer_class = serializers.ReportSerializer

    def get(self, request, pk):
        queryset = validator.is_report_owner(request, pk)
        
        serializer = serializers.ReportSerializer(queryset, many=False)
        return Response(serializer.data)


class NotificationListView(generics.ListCreateAPIView):
    serializer_class = serializers.NotificationSerializer
    
    def get(self, request):
        queryset = validator.can_get_notifications(request)
        serializer = serializers.NotificationSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        sender = validator.check_user(request)
        
        receiver = request.data['to']
        confirm_receiver = Auth.objects.get(email=receiver)
        if confirm_receiver:
            data = {
                'sender' : sender.first_name.title(),
                'receiver': confirm_receiver.first_name.title(),
                'message': request.data['message'],
                'message_status': 1,
            }

            serializer = serializers.NotificationSerializer(data=data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = request.data['message']
                mail.send_notification(sender.first_name.title(), receiver, message)

                return Response(serializer.data)
    

class NotificationDetailView(generics.RetrieveAPIView):
    lookup_field = 'pk'
    queryset = Notification.objects.all()
    serializer_class = serializers.NotificationSerializer

    def get(self, request, pk):
        queryset = validator.is_notification_owner(request, pk)
        serializer = serializers.NotificationSerializer(queryset, many=False)
        return Response(serializer.data)

