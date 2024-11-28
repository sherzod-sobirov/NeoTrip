from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


@admin.register(Country)
class CountryAdminModel(TranslationAdmin, admin.ModelAdmin):
    pass


@admin.register(IncludeExclude)
class IncludeExcludeAdminModel(TranslationAdmin, admin.ModelAdmin):
    pass


@admin.register(Destination)
class DestinationAdminModel(TranslationAdmin, admin.ModelAdmin):
    pass


@admin.register(Tour)
class TourAdminModel(TranslationAdmin, admin.ModelAdmin):
    list_display = ('title', 'duration', 'status')
    search_fields = ("title", )
    list_filter = ("status", )