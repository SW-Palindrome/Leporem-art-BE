from apps.exhibitions.repositories import ExhibitionRepository


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
