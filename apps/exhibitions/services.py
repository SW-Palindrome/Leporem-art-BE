import uuid

from django.core.exceptions import PermissionDenied

from apps.exhibitions.models import ExhibitionItemSound
from apps.exhibitions.repositories import ExhibitionItemRepository, ExhibitionRepository
from apps.items.repositories import ItemRepository
from apps.sellers.repositories import SellerRepository
from utils.files import create_presigned_url, create_random_filename


class ExhibitionService:
    def register(self, nickname, start_date, end_date):
        exhibition = ExhibitionRepository().register(
            nickname=nickname,
            start_date=start_date,
            end_date=end_date,
        )
        SellerRepository().change_temperature(exhibition.seller.seller_id, 5)

    def register_artist_info(
        self,
        exhibition_id,
        is_template,
        artist_image,
        biography=None,
        font_family=None,
        background_color=None,
    ):
        if is_template and not all([biography, font_family, background_color]):
            raise ValueError('템플릿을 사용할 경우, biography, font_family, background_color는 필수값입니다.')

        repository = ExhibitionRepository()

        if is_template:
            return repository.register_artist_info(
                exhibition_id,
                biography,
                artist_image,
                font_family,
                background_color,
            )

        return repository.register_custom_artist_info(
            exhibition_id,
            artist_image,
        )


class ExhibitionItemService:
    def register(
        self,
        exhibition_id,
        seller_id,
        is_custom,
        template,
        title,
        description,
        images,
        sound,
        position,
        background_color,
        font_family,
        is_sale,
        shorts_url,
        price,
        max_amount,
    ):
        if is_custom and template:
            raise ValueError('커스텀을 사용할 경우, template은 필수값이 아닙니다.')

        if not is_custom and not all([template, title, description, background_color, font_family]):
            raise ValueError('템플릿을 사용할 경우, template, title, description, background_color, font_family는 필수값입니다.')

        if is_sale and not all([title, description, shorts_url, price, max_amount]):
            raise ValueError('판매할 경우, title, description, shorts_url, price, amount는 필수값입니다.')

        if template and (template < 1 or template > 9):
            raise ValueError('template 번호는 1~9 사이의 값이어야 합니다.')

        for image in images:
            image.name = create_random_filename(image.name)

        exhibition_item = ExhibitionItemRepository().register(
            exhibition_id=exhibition_id,
            item=None,
            is_custom=is_custom,
            template=template,
            title=title,
            description=description,
            images=images,
            sound=sound,
            position=position,
            background_color=background_color,
            font_family=font_family,
            is_sale=is_sale,
        )

        images = [exhibition_image.image.open() for exhibition_image in exhibition_item.exhibition_images.all()]

        if is_sale:
            item = ItemRepository().register(
                seller_id=seller_id,
                price=price,
                max_amount=max_amount,
                title=title,
                description=description,
                shorts_url=shorts_url,
                thumbnail_image=images[0],
                images=images[1:],
                categories=[],
                colors=[],
                width=None,
                depth=None,
                height=None,
            )
            exhibition = ExhibitionRepository().get_exhibition(exhibition_id)
            item.start_date = exhibition.start_date
            item.end_date = exhibition.end_date
            item.save()
            exhibition_item.item = item
            exhibition_item.save()

            SellerRepository().change_temperature(seller_id, 0.5)

    def get_presigned_url_to_post_sound(self, extension='mp3'):
        return create_presigned_url(f'{ExhibitionItemSound.sound.field.upload_to}{str(uuid.uuid4())}.{extension}')

    def modify(
        self,
        seller_id,
        exhibition_id,
        exhibition_item_id,
        is_custom,
        template,
        title,
        description,
        images,
        sound,
        position,
        background_color,
        font_family,
        is_sale,
        shorts_url,
        price,
        current_amount,
    ):
        if is_custom and template:
            raise ValueError('커스텀을 사용할 경우, template은 필수값이 아닙니다.')

        if not is_custom and not all([template, title, description, background_color, font_family]):
            raise ValueError('템플릿을 사용할 경우, template, title, description, background_color, font_family는 필수값입니다.')

        if is_sale and not all([title, description, shorts_url, price, current_amount]):
            print(is_sale, title, description, shorts_url, price, current_amount)
            raise ValueError('판매할 경우, title, description, shorts_url, price, amount는 필수값입니다.')

        if template and (template < 1 or template > 9):
            raise ValueError('template 번호는 1~9 사이의 값이어야 합니다.')

        for image in images:
            image.name = create_random_filename(image.name)

        exhibition_item = ExhibitionItemRepository().modify(
            exhibition_id=exhibition_id,
            exhibition_item_id=exhibition_item_id,
            is_custom=is_custom,
            template=template,
            title=title,
            description=description,
            images=images,
            sound=sound,
            position=position,
            background_color=background_color,
            font_family=font_family,
            is_sale=is_sale,
        )

        images = [exhibition_image.image.open() for exhibition_image in exhibition_item.exhibition_images.all()]

        if exhibition_item.item and is_sale:
            ItemRepository().modify(
                item_id=exhibition_item.item.item_id,
                seller_id=seller_id,
                price=price,
                current_amount=current_amount,
                title=title,
                description=description,
                shorts_url=shorts_url,
                thumbnail_image=images[0],
                images=images[1:],
                categories=[],
                colors=[],
                width=None,
                depth=None,
                height=None,
            )
        elif exhibition_item.item and not is_sale:
            ItemRepository().delete(seller_id=seller_id, item_id=exhibition_item.item.item_id)
            exhibition_item.item = None
            exhibition_item.save()
            SellerRepository().change_temperature(seller_id, -0.5)
        elif not exhibition_item.item and is_sale:
            item = ItemRepository().register(
                seller_id=seller_id,
                price=price,
                max_amount=current_amount,
                title=title,
                description=description,
                shorts_url=shorts_url,
                thumbnail_image=images[0],
                images=images[1:],
                categories=[],
                colors=[],
                width=None,
                depth=None,
                height=None,
            )
            item.start_date = exhibition_item.exhibition.start_date
            item.end_date = exhibition_item.exhibition.end_date
            item.save()
            exhibition_item.item = item
            exhibition_item.save()
            SellerRepository().change_temperature(seller_id, 0.5)

    def delete(self, exhibition_item_id, user_id):
        exhibition_item = ExhibitionItemRepository().get_exhibition_item(exhibition_item_id)
        if not exhibition_item.exhibition.seller.user_id == user_id:
            raise PermissionDenied('본인의 전시만 삭제할 수 있습니다.')
        if exhibition_item.item:
            ItemRepository().delete(
                seller_id=exhibition_item.exhibition.seller.seller_id, item_id=exhibition_item.item.item_id
            )
        deleted_position = exhibition_item.position
        ExhibitionItemRepository().delete(exhibition_item_id, deleted_position)

        SellerRepository().change_temperature(exhibition_item.exhibition.seller.seller_id, -0.5)
