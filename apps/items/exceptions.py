class ViewedException(Exception):
    """최근 본 작품 오류"""


class ItemDoesNotExist(ViewedException):
    """작품 번호 오류"""


class BuyerDoesNotExist(ViewedException):
    """구매자 번호 오류"""
