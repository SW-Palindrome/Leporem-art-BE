from random import randint

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
