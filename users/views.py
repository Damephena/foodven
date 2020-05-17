from django.shortcuts import render
from django.db.models.base import ObjectDoesNotExist
from django.contrib.auth import authenticate, logout
from django.contrib.auth.hashers import check_password

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import Customer, Vendor, Auth
import users.serializers as serializers
# Create your views here.

class CustomerRegisterView(generics.CreateAPIView):
    serializer_class = serializers.CustomerRegisterSerializer

    def post(self, request, *args, **kwargs):
        customer = Auth.objects.filter(email__exact=request.data['email'].lower()).first()

        if customer:
            return Response({'error': 'Email already in use'})

        serializer = serializers.CustomerRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            customer = serializer.save()

            if customer:
                user = Customer.objects.get(email=request.data['email'].lower())
                to_email = request.data['email']
                subject = "Confirm Email to FoodVen"
                message = "Hello {} {}! \nYou are trying to sign up with this email: \n{}\n Kindly open this link to continue http://localhost:8000/customers/set-password/{}".format(user.first_name, user.last_name, user.email, user.id)
                from_email = "noreply@foodvend.com"

                Customer.email_user(self, subject, message, from_email, to_email )
                return Response(serializer.data)
        else:
            return Response(serializer.errors)


class CustomerSetPasswordView(generics.UpdateAPIView):
    lookup_field = 'pk'
    serializer_class = serializers.CustomerSetPasswordSerializer
    queryset = Customer.objects.all()

    def put(self, request, pk):
        customer = Customer.objects.get(pk=pk)

        if self.request.data['password'] == self.request.data['confirm_password']:
            # allow partial update
            serializer = serializers.CustomerSetPasswordSerializer(customer, data=self.request.data, partial=True)
            
            if serializer.is_valid(raise_exception=True):
                # use serializer update() method to accept instance/object (customer) & validated data
                serializer.update(customer, request.data['password'])
                # save new update
                serializer.save()

                data = {'id': customer.id, 'password': customer.password}
                return Response(data=data)
                # return Response({'message': 'Password successfully set!'})
        else:
            return Response({"error": "Password mismatch"})


class LoginView(APIView):
    
    permission_classes = []

    def post(self, request):
        email = request.data['email'].lower()
        password = request.data['password']
        user = authenticate(email=email, password=password)

        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({'error': 'Wrong credentials'})

    

class LogoutView(generics.RetrieveAPIView):
    def logout_view(self, request):
        logout(request)
        return Response({'message': 'Successfully logged out.'})


class VendorRegisterView(generics.CreateAPIView):
    serializer_class = serializers.VendorRegisterSerializer

    def post(self, request, *args, **kwargs):
        vendor = Auth.objects.filter(email__exact=request.data['email'].lower()).first()

        if vendor:
            return Response({'error': 'Email already in use'})

        serializer = serializers.VendorRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            vendor = serializer.save()

            if vendor:
                user = Vendor.objects.get(email=request.data['email'].lower())
                to_email = request.data['email']
                subject = "Confirm Email to FoodVen"
                message = "Hello {} {}! \nYou are trying to sign up as a vendor with this email: \n{}\nBusiness name: \n{}\nKindly open this link to continue http://localhost:8000/vendors/set-password/{}".format(user.first_name, user.last_name, user.email, user.business_name, user.id)
                from_email = "noreply@foodvend.com"

                Vendor.email_user(self, subject, message, from_email, to_email )
                return Response(serializer.data)
        else:
            return Response(serializer.errors)


class VendorSetPasswordView(generics.UpdateAPIView):
    lookup_field = 'pk'
    serializer_class = serializers.VendorSetPasswordSerializer
    queryset = Customer.objects.all()

    def put(self, request, pk):
        vendor = Vendor.objects.get(pk=pk)

        if self.request.data['password'] == self.request.data['confirm_password']:
            # allow partial update
            serializer = serializers.VendorSetPasswordSerializer(vendor, data=self.request.data, partial=True)
            
            if serializer.is_valid(raise_exception=True):
                # use serializer update() method to accept instance/object (vendor) & validated data
                serializer.update(vendor, request.data['password'])
                # save new update
                serializer.save()

                data = {'id': vendor.id, 'password': vendor.password}
                return Response(data=data)
        else:
            return Response({"error": "Password mismatch"})

