from typing import Optional

from apps.sellers.models import Seller
from apps.sellers.repositories import SellerRepository
from apps.users.models import User
from utils.email.aws import send_email


class SellerRegisterService:
    SENDER = 'email@leporem.art'

    def send_verify_email(self, user: User, email: str):
        verify_email = SellerRepository().create_verify_email(user=user, email=email)
        send_email(self.SENDER, email, '본인인증 이메일 요청', verify_email.verify_code)

    def verify(self, user: User, verify_code: str) -> Optional[Seller]:
        seller_repository = SellerRepository()
        verify_email = seller_repository.verify_code(user=user, verify_code=verify_code)
        if verify_email:
            return SellerRepository().register(user=user, email=verify_email.email)
        return None
