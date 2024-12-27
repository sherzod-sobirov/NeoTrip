import decimal
from django.db import models
import os
from core.settings import BASE_DIR
from ckeditor.fields import RichTextField  # Import RichTextField from ckeditor.fields


class Country(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return f"{self.name}"


class Destination(models.Model):
    country = models.ForeignKey("Country", on_delete=models.PROTECT)
    photo = models.ImageField(upload_to="destination/")
    city = models.CharField(max_length=256)
    about = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.city}"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the category
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-generated timestamp

    def __str__(self):
        return self.name

class Tour(models.Model):
    STATUS = (
        ("available", "Доступно"),
        ("archived", "в архиве"),
        ("discount", "скидка"),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="tours"  # This sets up the reverse relationship
    )
    photo = models.ImageField(upload_to="tour/")
    title = models.CharField(max_length=256)
    price = models.CharField(max_length=13, null=True, blank=True)  # 15 000 000 000.00
    duration = models.CharField(max_length=256)
    country = models.ForeignKey("Country", on_delete=models.PROTECT)
    overview = RichTextField()  # Use RichTextField for the rich text content
    status = models.CharField(max_length=30, choices=STATUS)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title}"

    @property
    def calc_disc(self):
        if self.status != "discount":
            return self.price
        return round(((100 - decimal.Decimal(self.discount)) / 100) * self.price, 2)

    @property
    def get_first_img(self):
        obj = self.tour_img.all()

        if obj:
            return self.tour_img.all().first().photo.url
        return None


