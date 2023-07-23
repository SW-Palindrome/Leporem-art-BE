from apps.buyers.models import Buyer


class BuyerRepository:
    def register(self, user_id):
        return Buyer.objects.create(user_id=user_id)

    def get_buyer(self, buyer_id):
        return Buyer.objects.get(buyer_id=buyer_id)
