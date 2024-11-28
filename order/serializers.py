from rest_framework import serializers
from .models import Order

class GeneratePayLinkSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    amount = serializers.IntegerField()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = 'created_at',