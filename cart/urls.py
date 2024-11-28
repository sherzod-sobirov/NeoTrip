from django.urls import path
from .views import *

urlpatterns = [
    path("cart/", CartListView.as_view(), name='cart_user_cart'),
    path("add-to-cart/<int:tour_id>/", AddToCartView.as_view(), name='cart_add_to_cart'),
]