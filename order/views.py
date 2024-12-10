from django.shortcuts import get_object_or_404, render
from django.views import View
from drf_yasg.utils import swagger_auto_schema
from payme.methods.generate_link import GeneratePayLink
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from tour.models import Tour
from order.serializers import GeneratePayLinkSerializer
from .models import Order
from .serializers import OrderSerializer
from django.shortcuts import redirect


class GeneratePayLinkAPIView(APIView):
    @swagger_auto_schema(
        request_body=GeneratePayLinkSerializer,
        responses={200: "{'pay_link': str}"}
    )
    def post(self, request, *args, **kwargs):
        """
        Generate a payment link for the given order ID and amount.

        Request parameters:
            - order_id (int): The ID of the order to generate a payment link for.
            - amount (int): The amount of the payment.

        Example request:
            curl -X POST \
                'http://your-host/shop/pay-link/' \
                --header 'Content-Type: application/json' \
                --data-raw '{
                "order_id": 999,
                "amount": 999
            }'

        Example response:
            {
                "pay_link": "http://payme-api-gateway.uz/bT0jcmJmZk1vNVJPQFFoP05GcHJtWnNHeH"
            }
        """
        serializer = GeneratePayLinkSerializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )
        pay_link = GeneratePayLink(**serializer.validated_data).generate_link()

        return Response({"pay_link": pay_link})


class MyOrdersView(View):
    def get(self, request):
        my_orders = Order.objects.filter(user=request.user)
        context = {
            'my_orders': my_orders
        }
        return render(request, 'user/my_orders.html', context)


class PaymentView(View):

    def perform_create(self, serializer):
        serializer.save()

    def get(self, request,tour_id=None):
        tour = get_object_or_404(Tour, id=tour_id)
        print(tour, request.user)
        serializer = OrderSerializer(data={'user': request.user.id,
                                           'amount': tour.price * 100,
                                           'tour': tour.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        pay_link = GeneratePayLink(
            order_id=serializer.data['id'],
            amount=serializer.data['amount'],
            callback_url=settings.PAYME['PAYME_CALL_BACK_URL']
        ).generate_link()
        print(serializer.data)

        data = {
            "link": "",
            "order": serializer.data
        }
        return redirect(pay_link)
