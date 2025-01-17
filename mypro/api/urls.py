from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('cartDetails/',views.CartApi.as_view(),name='cart'),
    path('gettoken/',views.UserAuthApi.as_view(),name='usertoken')
    ]
