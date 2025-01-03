# from django.shortcuts import render
from rest_framework.response import Response
from client.models import Toy,Category,Billingaddress,Deliveryaddress,Cart
from . import serializers
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework import filters
from django.contrib.auth.models import User
from rest_framework import generics
from .filters import UserCartFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from django.db.models import F,Sum

class ProductViewAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Toy.objects.prefetch_related('categoryId','subcategoryId')
    serializer_class=  serializers.ProductSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter,filters.SearchFilter]
    search_fields = ['name','description','categoryId__categoryName','subcategoryId__subcategoryName']
    ordering_fields = ['created_date']

    def get_serializer_context(self):
        # Pass the action explicitly to the serializer context
        context = super().get_serializer_context()
        context['action'] = self.action  # 'action' is automatically set by DRF (e.g., 'list', 'retrieve')
        return context

class CategoryViewAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()    
    serializer_class = serializers.CategorySerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().first()
        serializer = self.serializer_class()
        return Response(serializer.data)

    
    def get_queryset(self):
        return User.objects.filter(id = self.request.user.id)
    
    @action(detail=False, methods=['get'],url_path='billingaddress')
    def billingaddress(self,request):
        queryset = self.filter_queryset(self.get_queryset())
        billingAddress = Billingaddress.objects.get(uId=queryset.first().id)
        serializer = serializers.BillingAddressSerializer(billingAddress)
        if serializer:
            return Response(serializer.data)
        return Response(serializer.errors)
    
      
    @action(detail=False, methods=['get'],url_path='deliveryaddress')
    def billingaddress(self,request):
        queryset = self.filter_queryset(self.get_queryset())
        deliveryAddress = Deliveryaddress.objects.get(uId=queryset.first().id)
        serializer = serializers.DeliveryaddressSerializer(deliveryAddress)
        if serializer:
            return Response(serializer.data)
        return Response(serializer.errors)


class CartViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = serializers.CartSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [UserCartFilter]
  
    def list(self, request, *args, **kwargs):
        cart_items = self.filter_queryset(self.queryset)
        total = sum(item.subTotal or 0 for item in cart_items)
        serializer = self.get_serializer(cart_items, many=True)
        
        return Response({
            'cart_items': serializer.data, 
            'total': total  
        })
    
    @action(detail=False,methods=['GET'],url_path='price')
    def total(self,request):
        cart_items = self.filter_queryset(self.queryset)
        total = sum(item.subTotal or 0 for item in cart_items) 
        if total:
            return Response({'total':total})
        else:
            return Response({'Details':'No data found.'})

    # def retrieve(self, request, *args, **kwargs):
    #     raise MethodNotAllowed('GET', detail="Retrieve method is not allowed for this viewset.")
    

class CartView(APIView):

    def get(self,request):
        cart_items =  Cart.objects.filter(user = request.user)
        if cart_items:
            serializer = serializers.CartDetailSerializer(cart_items,many= True)
            total = cart_items.aggregate(total =Sum(F('quantity')*F('product__purchasePrice')))
            return Response({'cart_items':serializer.data,"total":total['total']})
        else:
            return Response({'Details':'No cart data found.'})


    






