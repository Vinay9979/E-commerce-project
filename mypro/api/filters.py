from rest_framework import filters
# from django.contrib.auth.models import User

class OwnUerFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(id=request.user.id)
    


class UserCartFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        cart_items = queryset.filter(user = request.user)
        if cart_items:
            return cart_items
        else:
            return {"Details":"No cart items found"}
            
        return queryset.filter(user=request.user)