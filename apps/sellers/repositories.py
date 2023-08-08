from random import randint

from django.db.models import Case, Count, F, OuterRef, Subquery, Sum, When
from django.db.models.functions import Round

from apps.orders.models import Order, OrderStatus, Review
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
        """총 거래횟수와 재구매희망률"""
        total_transactions = Subquery(
            Order.objects.filter(
                item__seller__seller_id=OuterRef('pk'), order_status__status=OrderStatus.Status.DELIVERED.value
            )
            .values('item__seller__seller_id')
            .annotate(total_transactions=Count('order_id'))
            .values('total_transactions')[:1]
        )

        retention_rate = Subquery(
            Review.objects.filter(
                order__item__seller__seller_id=OuterRef('pk'),
                order__order_status__status=OrderStatus.Status.DELIVERED.value,
            )
            .annotate(
                is_positive_review=Case(When(rating__gte=3, then=1), default=0),
            )
            .values('order__item__seller__seller_id')
            .annotate(
                total_positive_reviews=Sum('is_positive_review'),
                retention_rate=Round(100 * Sum('is_positive_review') / Count('order__order_id'), 1),
            )
            .values('retention_rate')[:1]
        )

        seller_info = (
            Seller.objects.select_related('user')
            .annotate(
                nickname=F('user__nickname'),
                item_count=Count('items'),
                total_transactions=total_transactions,
                retention_rate=retention_rate,
            )
            .get(seller_id=seller_id)
        )

        return seller_info

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

    def change_temperature(self, seller_id, number):
        seller = Seller.objects.get(seller_id=seller_id)
        seller.temperature += number
        if seller.temperature >= 100:
            seller.temperature = 100
        seller.save()
