from django.core.exceptions import ObjectDoesNotExist

from rest_framework import views, viewsets, generics
from rest_framework.response import Response

from .models import Order, Menu
from users.models import Customer, Vendor
import services.serializers as serializers

# Create your views here.

class MenuListView(generics.ListCreateAPIView):
    serializer_class = serializers.MenuSerializer

    def get(self, obj):
        queryset = Menu.objects.all()
        serializer = serializers.MenuSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            user = Vendor.objects.get(id=request.user.id)
        except (ObjectDoesNotExist, AssertionError):
            return Response({'error': 'You are not authenticated as a vendor'})
        else:
            data = {
                'vendor': user,
                'name': request.data['name'],
                'description': request.data['description'],
                'price': request.data['price'],
                # 'is_recurring': request.data['is_recurring'],
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
        except ObjectDoesNotExist:
            return Response({'error': 'Menu with given ID not found'})
        else:
            serializer = serializers.MenuSerializer(queryset, many=False)
            return Response(serializer.data)


    def put(self, request, pk):
        try:
            user = Menu.objects.filter(vendor=request.user, pk=pk).first()
        except (ObjectDoesNotExist, AssertionError):
            return Response({'error': 'You cannot update a menu you did not create'})
        else:
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
        try:
            user = Menu.objects.filter(vendor=request.user, id=pk).first()
        except AssertionError:
            return Response({'error': 'You cannot delete a menu you did not create'})
        except ObjectDoesNotExist:
            return Response({'error': 'Menu ID does not exist'})
        else:
            menu = Menu.objects.get(pk=pk)
            if menu.delete():
                return Response({'message': 'Menu deleted successfully!'})



class OrderListView(generics.ListAPIView):
    
    def get(self, request):
        menus = Menu.objects.all()
        return Response(menus)


class OrderCreateView(generics.CreateAPIView):
    def post(self, request):
        pass


class OrderDetailView(generics.RetrieveUpdateAPIView):
    queryset = Menu.objects.all()
    serializer_class = serializers.MenuSerializer

    