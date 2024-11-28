from payme.models import MerchantTransactionsModel
from payme.views import MerchantAPIView
from rest_framework import status
from rest_framework.response import Response

from .models import Order
from cart.models import Cart


# class PaymeCallBackAPIView(MerchantAPIView):
#     def create_transaction(self, order_id, action, *args, **kwargs) -> None:
#         print(f"create_transaction for order_id: {order_id}, response: {action}")
#         transaction = MerchantTransactionsModel.objects.filter(id=action['result']['transaction'])
#         if transaction.exists():
#             order = Order.objects.filter(id=order_id).first()
#             order.status = order.Status.PENDING
#             order.save(update_fields=['status'])
#
#     def perform_transaction(self, order_id, action, *args, **kwargs) -> None:
#         print(f"perform_transaction for order_id: {order_id}, response: {action}")
#         transaction = MerchantTransactionsModel.objects.filter(id=action['result']['transaction'])
#         if transaction.exists():
#             order = Order.objects.filter(id=order_id).first()
#             order.status = order.Status.PAID
#             order.save(update_fields=['status'])
#
#     def cancel_transaction(self, order_id, action, *args, **kwargs) -> None:
#         print(f"cancel_transaction for order_id: {order_id}, response: {action}")
#         transaction = MerchantTransactionsModel.objects.filter(id=action['result']['transaction'])
#         if transaction.exists():
#             order = Order.objects.filter(id=order_id).first()
#             order.status = order.Status.CANCELED
#             order.save(update_fields=['status'])


class PaymeCallBackAPIView(MerchantAPIView):
    def create_transaction(self, order_id, action, *args, **kwargs) -> None:
        print(f"create_transaction for order_id: {order_id}, response: {action}")
        transaction = MerchantTransactionsModel.objects.filter(transaction_id=action['result']['transaction'])
        if transaction.exists():
            order = Order.objects.filter(id=order_id).first()
            order.status = Order.Status.PENDING
            order.save()

    def perform_transaction(self, order_id, action, *args, **kwargs) -> None:
        print(f"perform_transaction for order_id: {order_id}, response: {action}")
        transaction = MerchantTransactionsModel.objects.filter(transaction_id=action['result']['transaction'])
        if transaction.exists():
            order = Order.objects.filter(id=order_id).first()
            order.status = Order.Status.PAID
            order.save()

    def cancel_transaction(self, order_id, action, *args, **kwargs) -> None:
        print(f"cancel_transaction for order_id: {order_id}, response: {action}")
        transaction = MerchantTransactionsModel.objects.filter(transaction_id=action['result']['transaction'])
        if transaction.exists():
            order = Order.objects.filter(id=order_id).first()
            order.status = Order.Status.CANCELED
            order.save()
