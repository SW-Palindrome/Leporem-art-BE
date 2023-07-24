from random import randint

from django.db.models import Count, F

from apps.sellers.models import Seller, VerifyEmail
from apps.users.models import User


class SellerRepository:
    def create_verify_email(self, user: User, email: str) -> VerifyEmail:
        verify_code = str(randint(100000, 999999))
        return VerifyEmail.objects.create(user=user, email=email, verify_code=verify_code)

    def verify_code(self, user: User, verify_code: str) -> VerifyEmail:
        return VerifyEmail.objects.filter(user=user, verify_code=verify_code).last()

    def register(self, user: User, email: str) -> Seller:
        user.is_seller = True
        user.save()
        return Seller.objects.create(user=user, email=email)

    def get_seller_info(self, seller_id):
        return (
            Seller.objects.select_related('user')
            .annotate(
                nickname=F('user__nickname'),
                item_count=Count('items'),
            )
            .get(seller_id=seller_id)
        )

    def get_seller_info_by_nickname(self, nickname):
        return (
            Seller.objects.select_related('user')
            .annotate(
                nickname=F('user__nickname'),
                item_count=Count('items'),
            )
            .get(user__nickname=nickname)
        )

    def change_description(self, seller_id, description):
        seller = Seller.objects.get(seller_id=seller_id)
        seller.description = description
        seller.save()
