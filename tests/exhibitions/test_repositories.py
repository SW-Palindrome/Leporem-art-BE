from datetime import date

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.exhibitions.models import Exhibition
from apps.exhibitions.repositories import ExhibitionRepository
from tests.sellers.factories import SellerFactory
from tests.users.factories import UserFactory


@pytest.mark.django_db
class TestExhibitionRepository:
    @pytest.fixture
    def user(self):
        return UserFactory(nickname='닉네임')

    @pytest.fixture
    def seller(self, user):
        return SellerFactory(user=user)

    def test_register(self, seller):
        exhibition_start_date = date(2023, 10, 1)
        exhibition_end_date = date(2023, 10, 8)
        sut = ExhibitionRepository()

        result = sut.register(seller.user.nickname, exhibition_start_date, exhibition_end_date)

        assert result == Exhibition.objects.get(
            seller=seller,
            start_date=date(2023, 10, 1),
            end_date=date(2023, 10, 8),
            artist_name='닉네임',
        )

    def test_register_artist_info(self, seller):
        exhibition = Exhibition.objects.create(
            seller=seller,
            start_date=date(2023, 10, 1),
            end_date=date(2023, 10, 8),
            artist_name=seller.user.nickname,
            is_template=False,
        )
        biography = '바이오그래피'
        artist_image = SimpleUploadedFile(
            name='artist_image.jpg',
            content=b'artist_image',
        )
        artist_image.name = 'artist_image.jpg'
        font_family = 'Pretandard'
        background_color = '#ffffff'
        sut = ExhibitionRepository()

        result = sut.register_artist_info(
            exhibition.exhibition_id,
            biography,
            artist_image,
            font_family,
            background_color,
        )

        assert result == Exhibition.objects.get(
            exhibition_id=exhibition.exhibition_id,
            start_date=date(2023, 10, 1),
            end_date=date(2023, 10, 8),
            biography='바이오그래피',
            is_template=True,
            font_family='Pretandard',
            background_color='#ffffff',
        )
        assert result.artist_image.name != 'artist_image.jpg'

    def test_register_custom_artist_info(self, seller):
        exhibition = Exhibition.objects.create(
            seller=seller,
            start_date=date(2023, 10, 1),
            end_date=date(2023, 10, 8),
            artist_name=seller.user.nickname,
            is_template=False,
        )
        artist_image = SimpleUploadedFile(
            name='artist_image.jpg',
            content=b'artist_image',
        )
        artist_image.name = 'artist_image.jpg'
        sut = ExhibitionRepository()

        result = sut.register_custom_artist_info(
            exhibition.exhibition_id,
            artist_image,
        )

        assert result == Exhibition.objects.get(
            exhibition_id=exhibition.exhibition_id,
            start_date=date(2023, 10, 1),
            end_date=date(2023, 10, 8),
            biography='',
            is_template=False,
            font_family='',
            background_color='',
        )
        assert result.artist_image.name != 'artist_image.jpg'

    def test_register_작가정보_입력_후_커스텀_이미지_사용(self, seller):
        exhibition = Exhibition.objects.create(
            seller=seller,
            start_date=date(2023, 10, 1),
            end_date=date(2023, 10, 8),
            artist_name=seller.user.nickname,
            is_template=False,
        )
        biography = '바이오그래피'
        artist_image = SimpleUploadedFile(
            name='artist_image.jpg',
            content=b'artist_image',
        )
        artist_image.name = 'artist_image.jpg'
        custom_image = SimpleUploadedFile(
            name='custom_image.jpg',
            content=b'custom_image',
        )
        custom_image.name = 'custom_image.jpg'
        font_family = 'Pretandard'
        background_color = '#ffffff'
        sut = ExhibitionRepository()

        sut.register_artist_info(
            exhibition.exhibition_id,
            biography,
            artist_image,
            font_family,
            background_color,
        )
        sut.register_custom_artist_info(
            exhibition.exhibition_id,
            custom_image,
        )

        assert Exhibition.objects.get(
            start_date=date(2023, 10, 1),
            end_date=date(2023, 10, 8),
            biography='',
            is_template=False,
            font_family='',
            background_color='',
        )
