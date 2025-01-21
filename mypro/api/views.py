# from django.shortcuts import render
from rest_framework.response import Response
from client.models import Toy,Category,Billingaddress,Deliveryaddress,Cart
from . import serializers
from rest_framework import viewsets
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework import filters
from django.contrib.auth.models import User
from rest_framework import generics
from .filters import UserCartFilter
from rest_framework.permissions import IsAuthenticated
from django.db.models import F,Sum
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.viewsets import ModelViewSet

# class CartApi(APIView):
#     # permission_classes =  [IsAuthenticated]
   
#     def get_queryset(self):
#         queryset = Cart.objects.all()
#         return queryset
    
#     def get(self,request):
#         cart_items = self.get_queryset()
#         total = cart_items.aggregate(total = Sum(F('product__purchasePrice'))) #filter(user = self.request.user)
#         total = total['total']
#         if cart_items.exists():
#             serializer  = serializers.CartSerializer(cart_items,total, many=True)
#             return Response(serializer.data)
#         else:
#             raise NotFound("No cart items found")
        
class TokenApi(APIView):

    def post(self,request):
        user = authenticate(request, username=request.data['username'], password=request.data['password'])
        if user :
            token,_ = Token.objects.get_or_create(user = user)
            return Response({"token":str(token)})
        return Response({'Details':'User does not exists'})
    

class ProductDetailApi(APIView):

    def get(self,request):
        if request.GET.get('product'):
            product = Toy.objects.filter(pk = request.GET['product'])
            if product.exists():
                serializer = serializers.ProductSerializer(product.first())
                return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class CartApi(APIView):

    def get(self,request):
        cart_items = Cart.objects.all()
        total = cart_items.aggregate(total = Sum('product__purchasePrice'))
        serializer = serializers.CartDetailSerializer(cart_items,many=True)
        print(total)

        return Response(
            {'cart_items':serializer.data,
             'total':total['total']
            }
        )

# class CategroryDetail(ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class  = serializers.CategorySerializer
#     def get_serializer_context(self):
#         return {'cart_items'}







