class OrderException(Exception):
    """주문 오류"""


class NotEnoughProductException(OrderException):
    """재고 부족 오류"""


class SelfOrderException(OrderException):
    """자기 자신 작품 구매 시도 오류"""


class InvalidOrderStatusException(OrderException):
    """주문 상태 오류"""


class OrderPermissionException(OrderException):
    """주문 품목에 대한 권한 오류"""


class ReviewException(Exception):
    """후기 오류"""


class InvalidOrderStatusReviewException(ReviewException):
    """주문 상태 오류"""


class InvalidOrderIDException(ReviewException):
    """주문 번호 오류"""


class IntegrityOrderIDException(ReviewException):
    """주문 번호 중복 오류"""
