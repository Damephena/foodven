from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from users.models import Vendor, Customer, Auth

from .models import Menu, Order, Report, OrderStatus, Notification, MessageStatus

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id','name', 'vendor', 'description', 'price', 'quantity', 'is_recurring']

    def create(self, validated_data):
        return Menu.objects.create(
            is_recurring=self.context['request'],
            **validated_data
        )
        

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        '''Cancel order'''
        
        if 'order_status' in validated_data:
            instance.order_status = OrderStatus.objects.get(id=4)
            instance.save()
            
            return instance


class OrderReadyStatusSerializer(serializers.ModelSerializer):
    '''Vendor updates order status to "ready"'''
    class Meta:
        model = Order
        fields = '__all__'

    def update(self, instance, validated_data):
        
        if 'order_status' in validated_data:
            instance.order_status = OrderStatus.objects.get(id=3)
            instance.save()
            
            return instance


class OrderProgressStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def update(self, instance, validated_data):
        
        if 'order_status' in validated_data:
            instance.order_status = OrderStatus.objects.get(id=2)
            instance.save()
            
            return instance

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields  = '__all__'


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'


class MessageStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageStatus
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'