from rest_framework.permissions import BasePermission, IsAuthenticated

from apps.chats.models import ChatRoom


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


class IsInChatRoom(IsAuthenticated):
    def has_object_permission(self, request, view, obj: ChatRoom):
        return bool(obj.buyer.user_id == request.user.user_id or obj.seller.user_id == request.user.user_id)
