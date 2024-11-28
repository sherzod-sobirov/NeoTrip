from collections.abc import Iterable
import decimal
from django.db import models
from tour.models import Tour


class Cart(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="cart")
    total = models.DecimalField(max_digits=13, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartitem")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="cartitemtour")
    count = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        price = self.tour.price
        if self.tour.status == "discount":
            price = self.tour.calc_disc
        cart = Cart.objects.get(id=self.cart.id)
        cart.total -= self.total
        self.total = decimal.Decimal(self.count) * price
        cart.total += self.total
        cart.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cart.id}"
