from apps.buyers.models import Buyer


class BuyerRepository:
    def register(self, user_id):
        buyer = Buyer.objects.create(user_id=user_id)
        return buyer
