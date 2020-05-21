from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Customer, Vendor, Auth

class CustomerRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number']
    
    def create(self, validated_data):
        email = validated_data['email']
        customer = Customer.objects.create(
            email=email.lower(), 
            first_name=validated_data['first_name'].title(),
            last_name=validated_data['last_name'].title(),
            phone_number=validated_data['phone_number']
            )
        return customer


class CustomerSetPasswordSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=500, required=True)

    class Meta:
        model = Auth
        fields = ['id', 'email', 'password', 'confirm_password']
        read_only_fields = ['email']
        extra_kwargs = { 
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        # Has to loop through data or else it would raise "string indices must be integers" error
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            instance.save()
            Token.objects.create(user=instance)
            return instance


class CustomerListSerializer(serializers.ModelSerializer):
    '''Serializer for any authenticated user'''
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number']


class CustomerProfileSerializer(serializers.ModelSerializer):
    '''Serializer for authenticated owner'''
    class Meta:
        model = Customer
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 
        'phone_number', 'amount_outstanding', 'date_joined'
        ]


class VendorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'business_name', 'email', 'first_name', 'last_name',  'phone_number']
    
    def create(self, validated_data):
        email = validated_data['email']
        vendor = Vendor.objects.create(
            email=email.lower(), 
            first_name=validated_data['first_name'].title(),
            last_name=validated_data['last_name'].title(),
            business_name=validated_data['business_name'].title(),
            phone_number=validated_data['phone_number']
            )
        return vendor


class VendorSetPasswordSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=500, required=True)

    class Meta:
        model = Auth
        fields = ['id', 'email', 'password', 'confirm_password']
        read_only_fields = ['email']
        extra_kwargs = { 
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        # Has to loop through data or else it would raise "string indices must be integers" error
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            instance.save()
            Token.objects.create(user=instance)
            return instance

class VendorListSerializer(serializers.ModelSerializer):
    '''Serializer for customers to view vendor list'''
    class Meta:
        model = Vendor
        fields = ['id', 'business_name', 'phone_number', 'email', 'first_name']

class VendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'email', 'business_name', 'password', 'phone_number', 'first_name', 'last_name', 'date_joined']

