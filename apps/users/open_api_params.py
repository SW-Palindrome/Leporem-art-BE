from drf_yasg import openapi

signup_get_params = [
    openapi.Parameter(
        '개인정보동의약관',
        openapi.IN_QUERY,
        description='약관내용',
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        '광고성정보동의약관',
        openapi.IN_QUERY,
        description='약관내용',
        type=openapi.TYPE_STRING,
    ),
]

signup_post_params = [
    openapi.Parameter(
        'is_agree_privacy',
        openapi.IN_QUERY,
        description='개인정보 동의여부입니다.',
        type=openapi.TYPE_BOOLEAN,
    ),
    openapi.Parameter(
        'is_agree_ads',
        openapi.IN_QUERY,
        description='광고성 정보 동의여부입니다.',
        type=openapi.TYPE_BOOLEAN,
    ),
    openapi.Parameter(
        'nickname',
        openapi.IN_QUERY,
        description="r'^[A-Za-z0-9가-힣_-]{2,10}$'",
        type=openapi.TYPE_STRING,
    ),
]

signin_params = [
    openapi.Parameter(
        'provider_id',
        openapi.IN_QUERY,
        description='존재여부 확인',
        type=openapi.TYPE_STRING,
    ),
]
