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


class IncludeExclude(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return f"{self.name}"


class Tour(models.Model):
    STATUS = (
        ("available", "Доступно"),
        ("archived", "в архиве"),
        ("discount", "скидка"),
    )
    photo = models.ImageField(upload_to="tour/")
    title = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=13, decimal_places=2)  # 15 000 000 000.00
    duration = models.CharField(max_length=256)
    person_count = models.IntegerField()
    country = models.ForeignKey("Country", on_delete=models.PROTECT)
    overview = RichTextField()  # Use RichTextField for the rich text content
    include = models.ManyToManyField("IncludeExclude", related_name="tour_include")
    exclude = models.ManyToManyField("IncludeExclude", related_name="tour_exclude")
    status = models.CharField(max_length=30, choices=STATUS)
    discount = models.FloatField(blank=True, null=True)
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


