class OrderException(Exception):
    """주문 오류"""


class NotEnoughProductException(OrderException):
    """재고 부족 오류"""


class SelfOrderException(OrderException):
    """자기 자신 작품 구매 시도 오류"""
