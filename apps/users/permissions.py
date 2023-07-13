from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_seller
