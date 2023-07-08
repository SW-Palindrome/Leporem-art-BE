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
]

get_params2 = [
    openapi.Parameter(
        'kakao_user',
        openapi.IN_QUERY,
        description='Kakao signup',
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        '닉네임',
        openapi.IN_QUERY,
        description='nickname입니다.',
        type=openapi.TYPE_OBJECT,
    ),
]
