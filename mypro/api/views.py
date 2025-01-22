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
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

        
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
            else:
                return Response({'Details':'No product Found'})
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








