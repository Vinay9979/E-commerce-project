from rest_framework import filters
# from django.contrib.auth.models import User

class OwnUerFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(id=request.user.id)
    


class UserCartFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)