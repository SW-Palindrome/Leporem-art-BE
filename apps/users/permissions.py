from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsBuyerOnly(BasePermission):
    """판매자가 아닌 구매자만 접근 가능"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and not request.user.is_seller)


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_seller)
