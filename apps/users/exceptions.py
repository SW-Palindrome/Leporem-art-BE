class DuplicateNicknameException(Exception):
    """닉네임 중복 예외"""


class DuplicateUserInfoException(Exception):
    """유저 정보 중복 예외"""


class ExpiredTokenException(Exception):
    """토큰 만료 예외"""
