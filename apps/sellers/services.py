import uuid
from typing import Optional

from apps.items.models import Item
from apps.items.repositories import ItemRepository
from apps.sellers.models import Seller
from apps.sellers.repositories import SellerRepository
from apps.users.models import User
from utils.email.aws import send_email
from utils.files import create_presigned_url, create_random_filename


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


class SellerService:
    def register_item(
        self,
        seller_id,
        price,
        max_amount,
        title,
        description,
        shorts_url,
        width,
        depth,
        height,
        thumbnail_image,
        images,
        categories,
        colors,
    ):
        item_repository = ItemRepository()

        thumbnail_image.name = create_random_filename(thumbnail_image.name)
        for image in images:
            image.name = create_random_filename(image.name)

        item_repository.register(
            seller_id=seller_id,
            price=price,
            max_amount=max_amount,
            title=title,
            description=description,
            shorts_url=shorts_url,
            width=width,
            depth=depth,
            height=height,
            thumbnail_image=thumbnail_image,
            images=images,
            categories=categories,
            colors=colors,
        )

    def modify_item(
        self,
        seller_id,
        item_id,
        price,
        current_amount,
        title,
        description,
        shorts,
        width,
        depth,
        height,
        thumbnail_image,
        images,
        categories,
        colors,
    ):
        item_repository = ItemRepository()

        shorts.name = create_random_filename(shorts.name)
        thumbnail_image.name = create_random_filename(thumbnail_image.name)
        for image in images:
            image.name = create_random_filename(image.name)

        item_repository.modify(
            seller_id=seller_id,
            item_id=item_id,
            price=price,
            current_amount=current_amount,
            title=title,
            description=description,
            shorts=shorts,
            width=width,
            depth=depth,
            height=height,
            thumbnail_image=thumbnail_image,
            images=images,
            categories=categories,
            colors=colors,
        )

    def get_presigned_url_to_post_shorts(self):
        return create_presigned_url(f'{Item.shorts.field.upload_to}{str(uuid.uuid4())}')

    def change_description(self, seller_id, description):
        seller_repository = SellerRepository()
        seller_repository.change_description(seller_id=seller_id, description=description)

    def change_current_amount(self, item_id, seller_id, action):
        item_repository = ItemRepository()
        item_repository.change_current_amount(item_id, seller_id, action)
