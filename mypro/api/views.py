# from django.shortcuts import render
from rest_framework.response import Response
from client.models import Toy,Category,Billingaddress,Deliveryaddress,Cart
from . import serializers
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
# from django_filters import rest_framework
# from django_filters
from rest_framework.views import APIView
from rest_framework import filters
from django.contrib.auth.models import User
from rest_framework import generics
from .filters import UserCartFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
# from rest_framework.exceptions import MethodNotAllowed
from django.db.models import F,Sum
from rest_framework import status



class UserAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            queryset = User.objects.get(id = request.user.id)
            serializer = serializers.UserSerializer(queryset)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'Detail':'No user Found'},status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
            data = request.data
            serializer = serializers.userDetailSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Details":'user has been created'})
            else:
                return Response(serializer.errors)

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


class CartViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = serializers.CartSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [UserCartFilter]
  
    def list(self, request, *args, **kwargs):
        cart_items = self.filter_queryset(self.queryset)
        if type(cart_items) == dict:
            return Response(cart_items)
        else:
            serializer = self.get_serializer(cart_items, many=True)
            total = sum(item.subTotal or 0 for item in cart_items)
            
            return Response({
                'cart_items': serializer.data, 
                'total': total  
            })
    
    @action(detail=False,methods=['GET'],url_path='price')
    def total(self,request):
        cart_items = self.filter_queryset(self.queryset)
        if type(cart_items) == dict:
            return Response({'Details':'No data found.'})
    
        total  = cart_items.aggregate(total = Sum('product__purchasePrice'))
        
        if total:
            return Response({'total':total['total']})
        else:
            return Response({'Details':'No data found.'})
    

class CartView(APIView):

    def get(self,request):
        cart_items =  Cart.objects.filter(user = request.user)
        if cart_items:
            serializer = serializers.CartDetailSerializer(cart_items,many= True)
            total = cart_items.aggregate(total =Sum(F('quantity')*F('product__purchasePrice')))
            return Response({'cart_items':serializer.data,"total":total['total']})
        else:
            return Response({'Details':'No cart data found.'})







