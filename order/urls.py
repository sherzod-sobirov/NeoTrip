from django.urls import path
from .views import *

urlpatterns = [
    path("my-orders/", MyOrdersView.as_view(), name='my_orders'),
    path("payment/<int:tour_id>", PaymentView.as_view(), name='payment')
]