from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('categories',views.CategroryDetail)

urlpatterns = [
    path('cartDetails/',views.CartApi.as_view(),name='cart'),
    path('gettoken/',views.TokenApi.as_view(),name='usertoken'),
    path('productdetail/',views.ProductDetailApi.as_view(),name='productdetail'),
    path('',include(router.urls))
]
