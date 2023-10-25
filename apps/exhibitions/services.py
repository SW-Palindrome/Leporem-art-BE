import uuid

from apps.exhibitions.models import ExhibitionItemSound
from apps.exhibitions.repositories import ExhibitionItemRepository, ExhibitionRepository
from apps.items.repositories import ItemRepository
from utils.files import create_presigned_url, create_random_filename


class ExhibitionService:
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
        categories,
        price,
        max_amount,
    ):
        if is_custom and template:
            raise ValueError('커스텀을 사용할 경우, template은 필수값이 아닙니다.')

        if not is_custom and not all([template, title, description, background_color, font_family]):
            raise ValueError('템플릿을 사용할 경우, template, title, description, background_color, font_family는 필수값입니다.')

        if is_sale and not all([title, description, shorts_url, categories, price, max_amount]):
            raise ValueError('판매할 경우, title, description, shorts, categories, price, max_amount는 필수값입니다.')

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
                categories=categories,
                colors=[],
                width=0,
                depth=0,
                height=0,
            )
            exhibition = ExhibitionRepository().get_exhibition(exhibition_id)
            item.start_date = exhibition.start_date
            item.end_date = exhibition.end_date
            item.save()
            exhibition_item.item = item
            exhibition_item.save()

    def get_presigned_url_to_post_sound(self, extension='mp3'):
        return create_presigned_url(f'{ExhibitionItemSound.sound.field.upload_to}{str(uuid.uuid4())}.{extension}')
