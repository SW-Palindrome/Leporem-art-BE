class ViewedException(Exception):
    """최근 본 작품 오류"""


class ItemDoesNotExist(ViewedException):
    """작품 번호 오류"""


class BuyerDoesNotExist(ViewedException):
    """구매자 번호 오류"""


class ItemException(Exception):
    """작품 오류"""


class CurrentAmountException(ItemException):
    """잔여 수량 오류"""
