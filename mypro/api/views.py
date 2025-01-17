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


class CartApi(APIView):
    permission_classes =  [IsAuthenticated]
    # authentication_classes=[TokenAuthentication]

    def get_queryset(self):
        queryset = Cart.objects.filter(user = self.request.user)
        return queryset
    
    def get(self,request):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer  = serializers.CartSerializer(queryset,many=True)
            return Response(serializer.data)
        else:
            raise NotFound("No cart items found")
        
class UserAuthApi(APIView):

    def post(self,request):
        user = User.objects.get(username = request.data['username'],password= request.data['password'])
        # print(user.first())
        if user:
            token = Token.objects.get_or_create(user = user)
            serializer = serializers.TokenSerializer(token)
            return Response(serializer.data)
        return Response({'Details':'User does not exists'})
    
    





