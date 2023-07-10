from drf_yasg import openapi

get_params = [
    openapi.Parameter(
        '1',
        openapi.IN_QUERY,
        description='개인정보 동의여부입니다.',
        type=openapi.TYPE_BOOLEAN,
    ),
    openapi.Parameter(
        '2',
        openapi.IN_QUERY,
        description='광고성 정보 동의여부입니다.',
        type=openapi.TYPE_BOOLEAN,
    ),
    openapi.Parameter(
        '닉네임',
        openapi.IN_QUERY,
        description="r'^[A-Za-z0-9가-힣_-]{2,10}$'",
        type=openapi.TYPE_STRING,
    ),
]
