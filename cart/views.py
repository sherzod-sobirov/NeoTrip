from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *


def cart_add(request):
    cart_item_id = request.POST.get("cart_item_id")
    cart_id = request.POST.get("cart_id")
    cart_item_id_obj = CartItem.objects.get(id=cart_item_id, cart_id=cart_id)
    cart_item_id_obj.count += 1
    cart_item_id_obj.save()


def cart_subtract(request):
    cart_item_id = request.POST.get("cart_item_id")
    cart_id = request.POST.get("cart_id")
    cart_item_id_obj = CartItem.objects.get(id=cart_item_id, cart_id=cart_id)
    cart_item_id_obj.count -= 1
    if cart_item_id_obj.count <= 0:
        CartItem.objects.filter(id=cart_item_id).delete()
    else:
        cart_item_id_obj.save()


class CartListView(View):
    template_name = "cart/cart.html"

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = []
        if not created:
            cart_items = CartItem.objects.filter(cart_id=cart.id)
        context = {
            'cart': cart,
            'cart_items': cart_items
        }
        return render(request, self.template_name, context)

    def post(self, request):
        cart_action = request.POST.get("cart_action")
        resp = {
            "-": cart_subtract,
            "+": cart_add,
        }
        resp[cart_action](request)
        total_item = CartItem.objects.filter(cart_id=request.POST.get("cart_id")).aggregate(total=Sum("total"))
        if "total" in total_item:
            Cart.objects.filter(id=request.POST.get("cart_id")).update(
                total=total_item['total'] if total_item['total'] is not None else 0
            )
        return redirect("cart_user_cart")


class AddToCartView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, tour_id):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_created = get_object_or_404(Cart, user=request.user)
        if not created:
            cart_item, cart_item_created = CartItem.objects.get_or_create(
                cart_id=cart.id,
                tour_id=tour_id
            )
            if not cart_item_created:
                cart_item.count += 1
                cart_item.save()
        else:
            CartItem.objects.get_or_create(
                cart_id=cart_created.id,
                tour_id=tour_id
            )
        return redirect("cart_user_cart")