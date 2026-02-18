from django.contrib import admin
from .models import Country, Destination, Category, Tour
from modeltranslation.admin import TranslationAdmin

# Country Admin
@admin.register(Country)
class CountryAdminModel(TranslationAdmin):
    list_display = ("name",)
    search_fields = ("name",)

# Destination Admin
@admin.register(Destination)
class DestinationAdminModel(TranslationAdmin):
    list_display = ("city", "country", "created_at")
    search_fields = ("city", "country__name")
    list_filter = ("country", "created_at")

# Category Admin
@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)

# Tour Admin
@admin.register(Tour)
class TourAdminModel(TranslationAdmin):
    list_display = ("title", "duration", "status", "price", "created_at")
    search_fields = ("title", "category__name")
    list_filter = ("status", "category", "created_at")
    ordering = ("-created_at",)
    