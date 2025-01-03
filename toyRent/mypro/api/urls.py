from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'productAPI',views.ProductViewAPI)
router.register(r'categoryAPI',views.CategoryViewAPI)
router.register(r'userAPI',views.UserViewSet)
router.register(r'cartAPI',views.CartViewSet)



urlpatterns = [
    path("",include(router.urls)),
    path('cartAPIVIEW/',views.CartView.as_view(),name='cartVIew')
]
