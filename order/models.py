from django.db import models
from tour.models import Tour
from user.models import User


# Create your models here.


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = "CREATED"
        PENDING = "PENDING"
        PAID = "PAID"
        CANCELED = "CANCELED"


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="orderitem")
    amount = models.DecimalField(max_digits=255, decimal_places=2)
    status = models.CharField(default=Status.CREATED, choices=Status.choices, max_length=20)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.tour.country)
    
